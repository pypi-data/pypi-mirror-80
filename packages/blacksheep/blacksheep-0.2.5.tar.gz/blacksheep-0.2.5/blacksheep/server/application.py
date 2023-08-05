import logging
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    Sequence,
)

from guardpost.asynchronous.authentication import AuthenticationStrategy
from guardpost.asynchronous.authorization import AuthorizationStrategy
from guardpost.authorization import Policy, UnauthorizedError
from rodi import Container, Services

from blacksheep.baseapp import BaseApplication
from blacksheep.common.files.asyncfs import FilesHandler
from blacksheep.contents import ASGIContent
from blacksheep.messages import Request, Response
from blacksheep.middlewares import get_middlewares_chain
from blacksheep.scribe import send_asgi_response
from blacksheep.server.authentication import (
    AuthenticateChallenge,
    get_authentication_middleware,
    handle_authentication_challenge,
)
from blacksheep.server.authorization import (
    AuthorizationWithoutAuthenticationError,
    get_authorization_middleware,
    handle_unauthorized,
)
from blacksheep.server.bindings import ControllerParameter
from blacksheep.server.controllers import router as controllers_router
from blacksheep.server.files.dynamic import ServeFilesOptions, serve_files_dynamic
from blacksheep.server.normalization import normalize_handler, normalize_middleware
from blacksheep.server.resources import get_resource_file_content
from blacksheep.server.routing import RegisteredRoute, Router, RoutesRegistry
from blacksheep.utils import ensure_bytes, join_fragments

ServicesType = Union[Services, Container]

__all__ = ("Application",)


def get_default_headers_middleware(
    headers: Sequence[Tuple[str, str]],
) -> Callable[..., Awaitable[Response]]:
    raw_headers = tuple((name.encode(), value.encode()) for name, value in headers)

    async def default_headers_middleware(
        request: Request, handler: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await handler(request)
        for name, value in raw_headers:
            response.add_header(name, value)
        return response

    return default_headers_middleware


class Resources:
    def __init__(self, error_page_html: str):
        self.error_page_html = error_page_html


class ApplicationEvent:
    def __init__(self, context: Any) -> None:
        self.__handlers: List[Callable[..., Any]] = []
        self.context = context

    def __iadd__(self, handler: Callable[..., Any]) -> "ApplicationEvent":
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler: Callable[..., Any]) -> "ApplicationEvent":
        self.__handlers.remove(handler)
        return self

    def __len__(self) -> int:
        return len(self.__handlers)

    async def fire(self, *args: Any, **keywargs: Any) -> None:
        for handler in self.__handlers:
            await handler(self.context, *args, **keywargs)


class ApplicationStartupError(RuntimeError):
    ...


class RequiresServiceContainerError(ApplicationStartupError):
    def __init__(self, details: str):
        super().__init__(
            f"The application requires services to be a Container "
            f"at this point of execution. Details: {details}"
        )
        self.details = details


class Application(BaseApplication):
    def __init__(
        self,
        *,
        router: Optional[Router] = None,
        resources: Optional[Resources] = None,
        services: Optional[ServicesType] = None,
        debug: bool = False,
        show_error_details: bool = False,
    ):
        if router is None:
            router = Router()
        if services is None:
            services = Container()
        super().__init__(show_error_details, router)

        if resources is None:
            resources = Resources(get_resource_file_content("error.html"))
        self.services: ServicesType = services
        self.debug = debug
        self.middlewares: List[Callable[..., Awaitable[Response]]] = []
        self.access_logger = None
        self.logger = None
        self._default_headers = None
        self._middlewares_configured = False
        self.resources = resources
        self._authentication_strategy: Optional[AuthenticationStrategy] = None
        self._authorization_strategy: Optional[AuthorizationStrategy] = None
        self.on_start = ApplicationEvent(self)
        self.on_stop = ApplicationEvent(self)
        self.started = False
        self.controllers_router: RoutesRegistry = controllers_router
        self.files_handler = FilesHandler()

    @property
    def default_headers(self) -> Optional[Tuple[Tuple[str, str], ...]]:
        return self._default_headers

    @default_headers.setter
    def default_headers(self, value: Optional[Tuple[Tuple[str, str], ...]]) -> None:
        self._default_headers = tuple(value) if value else None

    def use_authentication(
        self, strategy: Optional[AuthenticationStrategy] = None
    ) -> AuthenticationStrategy:
        if self.started:
            raise RuntimeError(
                "The application is already running, configure authentication "
                "before starting the application"
            )
        if not strategy:
            strategy = AuthenticationStrategy()

        self._authentication_strategy = strategy
        return strategy

    def use_authorization(
        self, strategy: Optional[AuthorizationStrategy] = None
    ) -> AuthorizationStrategy:
        if self.started:
            raise RuntimeError(
                "The application is already running, configure authorization "
                "before starting the application"
            )

        if not strategy:
            strategy = AuthorizationStrategy()

        if strategy.default_policy is None:
            # by default, a default policy is configured with no requirements,
            # meaning that request handlers allow anonymous users, unless
            # specified otherwise
            # this can be modified, by adding a requirement to the default
            # policy
            strategy.default_policy = Policy("default")

        self._authorization_strategy = strategy
        self.exceptions_handlers[
            AuthenticateChallenge
        ] = handle_authentication_challenge
        self.exceptions_handlers[UnauthorizedError] = handle_unauthorized
        return strategy

    def route(
        self, pattern: str, methods: Optional[Sequence[str]] = None
    ) -> Callable[..., Any]:
        if methods is None:
            methods = ["GET"]

        def decorator(f):
            for method in methods:
                self.router.add(method, pattern, f)
            return f

        return decorator

    def serve_files(self, options: ServeFilesOptions):
        serve_files_dynamic(self.router, self.files_handler, options)

    def _apply_middlewares_in_routes(self):
        for route in self.router:
            route.handler = get_middlewares_chain(self.middlewares, route.handler)

    def _normalize_middlewares(self):
        self.middlewares = [
            normalize_middleware(middleware, self.services)  # type: ignore
            for middleware in self.middlewares
        ]

    def use_controllers(self):
        # NB: controller types are collected here, and not with
        # Controller.__subclasses__(),
        # to avoid funny bugs in case several Application objects are defined
        # with different controllers; this is the case for example of tests.

        # This sophisticated approach, using metaclassing, dynamic
        # attributes, and calling handlers dynamically
        # with activated instances of controllers; still supports custom
        # and generic decorators (*args, **kwargs);
        # as long as `functools.wraps` decorator is used in those decorators.
        self.register_controllers(self.prepare_controllers())

    def get_controller_handler_pattern(
        self, controller_type: Type, route: RegisteredRoute
    ) -> bytes:
        """
        Returns the full pattern to be used for a route handler,
        defined as controller method.
        """
        base_route = getattr(controller_type, "route", None)

        if base_route is not None:
            if callable(base_route):
                value = base_route()
            elif isinstance(base_route, (str, bytes)):
                value = base_route
            else:
                raise RuntimeError(
                    f"Invalid controller `route` attribute. "
                    f"Controller `{controller_type.__name__}` "
                    f"has an invalid route attribute: it should "
                    f"be callable, or str, or bytes."
                )

            if value:
                return ensure_bytes(join_fragments(value, route.pattern))
        return ensure_bytes(route.pattern)

    def prepare_controllers(self) -> List[Type]:
        controller_types = []
        for route in self.controllers_router:
            handler = route.handler
            controller_type = getattr(handler, "controller_type")
            controller_types.append(controller_type)
            handler.__annotations__["self"] = ControllerParameter[controller_type]
            self.router.add(
                route.method,
                self.get_controller_handler_pattern(controller_type, route),
                handler,
            )
        return controller_types

    def bind_controller_type(self, controller_type: Type):
        templates_environment = getattr(self, "templates_environment", None)

        if templates_environment:
            setattr(controller_type, "templates", templates_environment)

    def register_controllers(self, controller_types: List[Type]):
        """
        Registers controller types as transient services
        in the application service container.
        """
        if not controller_types:
            return

        if not isinstance(self.services, Container):
            raise RequiresServiceContainerError(
                "When using controllers, the application.services must be "
                "a service `Container` (`rodi.Container`; not a built service "
                "provider)."
            )

        for controller_class in controller_types:
            if controller_class in self.services:
                continue

            self.bind_controller_type(controller_class)

            # TODO: maybe rodi should be modified to handle the following
            # internally;
            # if a type does not define an __init__ method, then a fair
            # assumption is that it can be instantiated
            # by calling it;
            # TODO: the following if statement can be removed if rodi is
            # modified as described above.
            if getattr(controller_class, "__init__") is object.__init__:
                self.services.add_transient_by_factory(
                    controller_class, controller_class
                )
            else:
                self.services.add_exact_transient(controller_class)

    def normalize_handlers(self):
        configured_handlers = set()

        self.router.sort_routes()

        for route in self.router:
            if route.handler in configured_handlers:
                continue

            route.handler = normalize_handler(route, self.services)
            configured_handlers.add(route.handler)
        configured_handlers.clear()

    def configure_middlewares(self):
        if self._middlewares_configured:
            return
        self._middlewares_configured = True

        if self._authorization_strategy:
            if not self._authentication_strategy:
                raise AuthorizationWithoutAuthenticationError()
            self.middlewares.insert(
                0, get_authorization_middleware(self._authorization_strategy)
            )

        if self._authentication_strategy:
            self.middlewares.insert(
                0, get_authentication_middleware(self._authentication_strategy)
            )

        if self._default_headers:
            self.middlewares.insert(
                0, get_default_headers_middleware(self._default_headers)
            )

        self._normalize_middlewares()

        if self.middlewares:
            self._apply_middlewares_in_routes()

    def build_services(self):
        if isinstance(self.services, Container):
            self.services = self.services.build_provider()

    async def start(self):
        if self.started:
            return

        self.started = True
        if self.on_start:
            await self.on_start.fire()

        self.use_controllers()
        self.build_services()
        self.normalize_handlers()
        self.configure_middlewares()

    async def stop(self):
        await self.on_stop.fire()
        self.started = False

    async def _handle_lifespan(self, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"

        try:
            await self.start()
        except:  # NOQA
            logging.exception("Startup error")
            await send({"type": "lifespan.startup.failed"})
            return

        await send({"type": "lifespan.startup.complete"})

        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        await self.stop()
        await send({"type": "lifespan.shutdown.complete"})

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            return await self._handle_lifespan(receive, send)

        assert scope["type"] == "http"

        request = Request.incoming(
            scope["method"], scope["raw_path"], scope["query_string"], scope["headers"]
        )
        request.scope = scope
        request.content = ASGIContent(receive)

        response = await self.handle(request)
        await send_asgi_response(response, send)

        request.scope = None  # type: ignore
        request.content.dispose()
