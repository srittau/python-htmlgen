from typing import Union, AnyStr, Generator

from htmlgen.element import Element


class Section(Element):
    def __init__(self) -> None: ...

class Article(Element):
    def __init__(self) -> None: ...

class Navigation(Element):
    def __init__(self) -> None: ...

class Aside(Element):
    def __init__(self) -> None: ...

class Header(Element):
    def __init__(self) -> None: ...

class Footer(Element):
    def __init__(self) -> None: ...

class Heading(Element):

    def __init__(self, level: int = ..., *content: Union[AnyStr, Generator]) -> None: ...
