from typing import Optional

from .element import VoidElement


class Image(VoidElement):
    url = ...  # type: str
    alternate_text = ...  # type: Optional[str]
    title = ...  # type: Optional[str]
    def __init__(self, url:  str, alternate_text: Optional[str] = ...) -> None: ...
