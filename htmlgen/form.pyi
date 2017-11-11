import datetime
from typing import List, Union, AnyStr, Optional

from htmlgen.element import Element, VoidElement
from htmlgen.generator import Generator


class Form(Element):
    method = ...  # type: str
    url = ...  # type: str
    target = ...  # type: str
    encryption_type = ...  # type: str
    multipart = ...  # type: bool
    def __init__(self, method: str = ..., url: str = ...) -> None: ...
    def set_blank_target(self) -> None: ...

class Input(VoidElement):
    name = ...  # type: str
    value = ...  # type: str
    readonly = ...  # type: bool
    disabled = ...  # type: bool
    type = ...  # type: str
    placeholder = ...  # type: Optional[str]
    size = ...  # type: Optional[int]
    focus = ...  # type: bool
    def __init__(self, type_: str = ..., name: str = ...) -> None: ...

class TextInput(Input):
    def __init__(self, name: str = ..., value: str = ...) -> None: ...

class SearchInput(Input):
    def __init__(self, name: str = ...) -> None: ...

class PasswordInput(Input):
    def __init__(self, name: str = ...) -> None: ...

class NumberInput(Input):
    number = ...  # type: Optional[float]
    minimum = ... # type: Optional[float]
    maximum = ...  # type: Optional[float]
    step = ...  # type: Optional[float]
    def __init__(self, name: str = ..., number: Optional[float] = ...) -> None: ...

class DateInput(Input):
    date = ...  # type: Optional[datetime.date]
    def __init__(self, name: str = ..., date: Optional[datetime.date] = ...) -> None: ...

class TimeInput(Input):
    time = ...  # type: Optional[datetime.time]
    minimum = ...  # type: Optional[datetime.time]
    maximum = ...  # type: Optional[datetime.time]
    step = ...  # type: Optional[float]
    def __init__(self, name: str = "", time: Optional[datetime.time] = ...) -> None: ...

class Checkbox(Input):
    checked = ...  # type: bool
    def __init__(self, name: str = ..., value: str = ...) -> None: ...

class RadioButton(Input):
    checked = ...  # type: bool
    def __init__(self, name: str = ..., value: str = ...) -> None: ...

class FileInput(Input):
    max_length = ...  # type: Optional[int]
    accept = ...  # type: List[str]
    def __init__(self, name: str = ...) -> None: ...

class HiddenInput(Input):
    def __init__(self, name: str, value: str) -> None: ...

class SubmitButton(Input):
    label = ...  # type: str
    def __init__(self, label: str) -> None: ...

class Button(Element):
    def __init__(self, *content: Union[AnyStr, Generator]) -> None: ...

class TextArea(Element):
    name = ...  # type: str
    readonly = ...  # type: bool
    disabled = ...  # type: bool
    columns = ...  # type: Optional[int]
    rows = ...  # type: Optional[int]
    placeholder = ...  # type: Optional[str]
    def __init__(self, name: str = ...) -> None: ...

class Select(Element):
    name = ...  # type: str
    disabled = ...  # type: bool
    selected_option = ...  # type: Optional[Option]
    selected_value = ...  # type: Optional[str]
    def __init__(self, name: str = "") -> None: ...
    def create_group(self, label: str) -> "OptionGroup": ...
    def create_option(self, label: str, value: Optional[str] = ..., selected: bool = ...) -> "Option": ...

class OptionGroup(Element):
    label = ...  # type: Optional[str]
    disabled = ...  # type: bool
    def __init__(self, label: str) -> None: ...
    def create_option(self, label: str, value: Optional[str] = ...) -> "Option": ...

class Option(Element):
    value = ...  # type: Optional[str]
    disabled = ...  # type: bool
    selected = ...  # type: bool
    def __init__(self, label: str, value: Optional[str] = None) -> None: ...

class Label(Element):
    for_ = ...  # type: Optional[str]
    def __init__(self, *children: Union[AnyStr, Generator]) -> None: ...
