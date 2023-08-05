import json
from typing import Any, Callable, Dict, Generator, List, Optional, Union

from guardpost.authentication import Identity, User

from .contents import Content, FormPart
from .cookies import Cookie
from .headers import Headers, HeaderType
from .url import URL
from .asgi import ASGIScopeInterface


class Message:
    @property
    def headers(self) -> Headers:
        ...

    def content_type(self) -> bytes:
        ...

    def get_first_header(self, key: bytes) -> bytes:
        ...

    def get_headers(self, key: bytes) -> List[bytes]:
        ...

    def get_single_header(self, key: bytes) -> bytes:
        ...

    def remove_header(self, key: bytes) -> None:
        ...

    def has_header(self, key: bytes) -> bool:
        ...

    def add_header(self, name: bytes, value: bytes) -> None:
        ...

    def set_header(self, key: bytes, value: bytes) -> None:
        ...

    async def read(self) -> Optional[bytes]:
        ...

    async def stream(self) -> Generator[bytes, None, None]:
        ...

    async def text(self) -> str:
        ...

    async def form(self) -> Union[Dict[str, str], Dict[str, List[str]], None]:
        """
        Returns values read either from multipart or www-form-urlencoded
        payload.

        This function adopts some compromises to provide a consistent api,
        returning a dictionary of key: values pairs.
        If a key is unique, the value is a single string; if a key is
        duplicated (licit in both form types), the value is a list of strings.

        Multipart form parts values that can be decoded as UTF8 are decoded,
        otherwise kept as raw bytes.
        In case of ambiguity, use the dedicated `multiparts()` method.
        """

    async def multipart(self) -> List[FormPart]:
        """
        Returns parts read from multipart/form-data, if present, otherwise
        None
        """

    def declares_content_type(self, type: bytes) -> bool:
        ...

    def declares_json(self) -> bool:
        ...

    def declares_xml(self) -> bool:
        ...

    async def files(self, name: Optional[str] = None) -> List[FormPart]:
        ...

    async def json(self, loads: Callable[[str], Any] = json.loads) -> Any:
        ...

    def has_body(self) -> bool:
        ...

    @property
    def charset(self) -> str:
        ...


Cookies = Dict[str, Cookie]


def method_without_body(method: str) -> bool:
    ...


class Request(Message):
    def __init__(self, method: str, url: bytes, headers: Optional[List[HeaderType]]) -> None:
        self.method: str = ...
        self._url: URL = ...
        self.route_values: Optional[Dict[str, str]] = ...
        self.content: Optional[Content] = ...
        self.identity: Union[None, Identity, User] = ...
        self.scope: ASGIScopeInterface = ...

    @classmethod
    def incoming(
        cls, method: str, path: bytes, query: bytes, headers: List[HeaderType]
    ) -> "Request":
        ...

    @property
    def query(self) -> Dict[str, List[str]]:
        ...

    @property
    def url(self) -> URL:
        ...

    @url.setter
    def url(self, value: Union[URL, bytes, str]) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def cookies(self) -> Cookies:
        ...

    def get_cookies(self) -> Cookies:
        ...

    def get_cookie(self, name: bytes) -> Optional[Cookie]:
        ...

    def set_cookie(self, cookie: Cookie) -> None:
        ...

    def set_cookies(self, cookies: List[Cookie]) -> None:
        ...

    @property
    def etag(self) -> Optional[bytes]:
        ...

    @property
    def if_none_match(self) -> Optional[bytes]:
        ...

    def expect_100_continue(self) -> bool:
        ...

    def with_content(self, content: Content) -> "Request":
        ...


class Response(Message):
    def __init__(
        self,
        status: int,
        headers: Optional[List[HeaderType]] = None,
        content: Optional[Content] = None,
    ) -> None:
        self.__headers = headers or []
        self.status = status
        self.content = content

    def __repr__(self) -> str:
        ...

    @property
    def cookies(self) -> Cookies:
        ...

    @property
    def reason(self) -> str:
        ...

    def get_cookies(self) -> Cookies:
        ...

    def get_cookie(self, name: bytes) -> Optional[Cookie]:
        ...

    def set_cookie(self, cookie: Cookie) -> None:
        ...

    def set_cookies(self, cookies: List[Cookie]) -> None:
        ...

    def unset_cookie(self, name: bytes) -> None:
        ...

    def remove_cookie(self, name: bytes) -> None:
        ...

    def is_redirect(self) -> bool:
        ...

    def with_content(self, content: Content) -> "Response":
        ...
