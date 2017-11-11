from typing import Union, AnyStr

from htmlgen.element import Element, VoidElement
from htmlgen.generator import Generator


class Span(Element):
    def __init__(self, *content: Union[AnyStr, Generator]) -> None: ...

class Highlight(Element):
    def __init__(self, *content: Union[AnyStr, Generator]) -> None: ...

class Strong(Element):
    def __init__(self, *content: Union[AnyStr, Generator]) -> None: ...

class Alternate(Element):
    def __init__(self, *content: Union[AnyStr, Generator]) -> None: ...

class Emphasis(Element):
    def __init__(self, *content: Union[AnyStr, Generator]) -> None: ...

class Small(Element):
    def __init__(self, *content: Union[AnyStr, Generator]) -> None: ...

class LineBreak(VoidElement):
    def __init__(self) -> None: ...
