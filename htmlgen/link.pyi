from typing import Optional, Union, AnyStr

from htmlgen.element import Element
from htmlgen.generator import Generator


class Link(Element):
    url = ...  # type: Optional[str]
    target = ...  # type: str
    title = ...  # type: Optional[str]
    def __init__(self, url: Optional[str], *content: Union[AnyStr, Generator]) -> None: ...
    def set_blank_target(self) -> None: ...
