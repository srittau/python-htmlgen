from typing import Union

from htmlgen.element import Element
from htmlgen.generator import Generator


class Division(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class Paragraph(Element):
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class Preformatted(Element):
    def __init__(self) -> None: ...
