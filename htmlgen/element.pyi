from collections.abc import Sized
import typing
from typing import Any, Mapping, Union, TypeVar, Set, Optional, overload

from htmlgen.generator import Generator, HTMLChildGenerator

_T = TypeVar("_T")

def is_element(o: Any, element_name: str) -> bool: ...

class _ElementDataProxy:
    def __init__(self, element: ElementBase) -> None: ...
    def __iter__(self) -> typing.Generator[str, None, None]: ...
    def __len__(self) -> int: ...
    def __setitem__(self, key: str, value: str) -> None: ...
    def __getitem__(self, key: str) -> str: ...
    def __delitem__(self, key: str) -> None: ...
    def clear(self) -> None: ...
    @classmethod
    def from_data(
        cls, element: ElementBase, data: Mapping[str, str]
    ) -> _ElementDataProxy: ...

class ElementBase(Generator):
    id: Optional[str]
    element_name: str
    @property
    def data(self) -> _ElementDataProxy: ...
    @data.setter
    def data(self, data: Mapping[str, str]) -> None: ...
    def __init__(self, element_name: str) -> None: ...
    def set_attribute(self, name: str, value: str) -> None: ...
    @overload
    def get_attribute(self, name: str) -> Optional[str]: ...
    @overload
    def get_attribute(self, name: str, default: _T) -> Union[str, _T]: ...
    def remove_attribute(self, name: str) -> None: ...
    @property
    def attribute_names(self) -> Set[str]: ...
    def add_css_classes(self, *css_classes: str) -> None: ...
    def remove_css_classes(self, *css_classes: str) -> None: ...
    def has_css_class(self, css_class: str) -> bool: ...
    def set_style(self, name: str, value: str) -> None: ...
    def render_start_tag(self) -> str: ...

class NonVoidElement(ElementBase):
    def generate_children(
        self
    ) -> typing.Generator[Union[str, bytes, Generator], None, None]: ...

class Element(NonVoidElement, Sized):
    children: HTMLChildGenerator
    def __init__(self, element_name: str) -> None: ...
    def __bool__(self) -> bool: ...
    def __getattr__(self, item: str) -> Any: ...
    def __len__(self) -> int: ...
    def __nonzero__(self) -> bool: ...

class VoidElement(ElementBase): ...
