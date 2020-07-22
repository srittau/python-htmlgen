from enum import Enum
from typing import Optional

from htmlgen import Element

class Preload(Enum):
    NONE: str
    METADATA: str
    AUTO: str


class Video(Element):
    controls: bool
    poster: Optional[str]
    preload: Optional[Preload]
    def __init__(self, src: str) -> None: ...
