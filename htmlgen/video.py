from enum import Enum

from .attribute import boolean_html_attribute, html_attribute, enum_attribute
from .element import Element


class Preload(Enum):
    NONE = "none"
    METADATA = "metadata"
    AUTO = "auto"


class Video(Element):
    controls = boolean_html_attribute("controls")
    poster = html_attribute("poster")
    preload = enum_attribute("preload", Preload)

    def __init__(self, src: str) -> None:
        super().__init__("video")
        self.set_attribute("src", src)
