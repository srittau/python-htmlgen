from typing import Union

from htmlgen.element import Element, VoidElement
from htmlgen.generator import Generator


class Span(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class Highlight(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class Strong(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class Alternate(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class Emphasis(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class Small(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class LineBreak(VoidElement):
    def __init__(self) -> None: ...
