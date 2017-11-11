import datetime
from typing import Union

from htmlgen.element import Element

class Time(Element):
    def __init__(self, date: Union[datetime.datetime, datetime.time]) -> None: ...
