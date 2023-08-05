from collections.abc import MutableSequence
from typing import Union, Dict, List, Tuple, Optional, Generator


class Header:
    def __init__(self, name: bytes, value: bytes):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        ...

    def __iter__(self) -> Generator[bytes, None, None]:
        ...

    def __eq__(self, other: object) -> bool:
        ...


HeaderType = Tuple[bytes, bytes]


class Headers:
    def __init__(self, values: Optional[List[HeaderType]] = None):
        self.values = values

    def get(self, name: bytes) -> Tuple[HeaderType]:
        ...

    def get_tuples(self, name: bytes) -> List[HeaderType]:
        ...

    def get_first(self, key: bytes) -> bytes:
        ...

    def get_single(self, key: bytes) -> bytes:
        ...

    def merge(self, values: List[HeaderType]):
        ...

    def update(self, values: Dict[bytes, bytes]):
        ...

    def items(self) -> Generator[HeaderType, None, None]:
        ...

    def clone(self) -> "Headers":
        ...

    def add_many(self, values: Union[Dict[bytes, bytes], List[Tuple[bytes, bytes]]]):
        ...

    def __add__(self, other: Union["Headers", Header, HeaderType, MutableSequence]):
        ...

    def __radd__(self, other: Union["Headers", Header, HeaderType, MutableSequence]):
        ...

    def __iadd__(self, other: Union["Headers", Header, HeaderType, MutableSequence]):
        ...

    def __iter__(self) -> Generator[HeaderType, None, None]:
        ...

    def __setitem__(self, key: bytes, value: bytes):
        ...

    def __getitem__(self, item: bytes):
        ...

    def keys(self) -> Tuple[bytes]:
        ...

    def add(self, name: bytes, value: bytes):
        ...

    def set(self, name: bytes, value: bytes):
        ...

    def remove(self, key: bytes):
        ...

    def contains(self, key: bytes) -> bool:
        ...

    def __delitem__(self, key: bytes):
        ...

    def __contains__(self, key: bytes) -> bool:
        ...

    def __repr__(self) -> str:
        ...
