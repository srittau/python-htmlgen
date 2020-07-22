import datetime
from enum import Enum
from typing import List, Union, Optional

from htmlgen.element import Element, VoidElement
from htmlgen.generator import Generator

class Autocomplete(Enum):
    OFF: str
    ON: str

class Form(Element):
    method: str
    url: str
    target: str
    encryption_type: str
    autocomplete: Optional[Autocomplete]
    multipart: bool
    def __init__(self, method: str = ..., url: str = ...) -> None: ...
    def set_blank_target(self) -> None: ...

class Input(VoidElement):
    name: str
    value: str
    readonly: bool
    disabled: bool
    type: str
    autocomplete: Optional[str]
    placeholder: Optional[str]
    size: Optional[int]
    focus: bool
    def __init__(self, type_: str = ..., name: str = ...) -> None: ...

class TextInput(Input):
    def __init__(self, name: str = ..., value: str = ...) -> None: ...

class SearchInput(Input):
    def __init__(self, name: str = ...) -> None: ...

class PasswordInput(Input):
    def __init__(self, name: str = ...) -> None: ...

class NumberInput(Input):
    number: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]
    step: Optional[float]
    def __init__(
        self, name: str = ..., number: Optional[float] = ...
    ) -> None: ...

class DateInput(Input):
    date: Optional[datetime.date]
    def __init__(
        self, name: str = ..., date: Optional[datetime.date] = ...
    ) -> None: ...

class TimeInput(Input):
    time: Optional[datetime.time]
    minimum: Optional[datetime.time]
    maximum: Optional[datetime.time]
    step: Optional[float]
    def __init__(
        self, name: str = "", time: Optional[datetime.time] = ...
    ) -> None: ...

class Checkbox(Input):
    checked: bool
    def __init__(self, name: str = ..., value: str = ...) -> None: ...

class RadioButton(Input):
    checked: bool
    def __init__(self, name: str = ..., value: str = ...) -> None: ...

class FileInput(Input):
    max_length: Optional[int]
    accept: List[str]
    def __init__(self, name: str = ...) -> None: ...

class HiddenInput(Input):
    def __init__(self, name: str, value: str) -> None: ...

class SubmitButton(Input):
    label: str
    def __init__(self, label: str) -> None: ...

class Button(Element):
    disabled: bool
    def __init__(self, *content: Union[str, bytes, Generator]) -> None: ...

class TextArea(Element):
    name: str
    readonly: bool
    disabled: bool
    columns: Optional[int]
    rows: Optional[int]
    autocomplete: Optional[str]
    placeholder: Optional[str]
    def __init__(self, name: str = ...) -> None: ...

class Select(Element):
    name: str
    disabled: bool
    autocomplete: Optional[str]
    selected_option: Optional[Option]
    selected_value: Optional[str]
    def __init__(self, name: str = ...) -> None: ...
    def create_group(self, label: str) -> OptionGroup: ...
    def create_option(
        self, label: str, value: Optional[str] = ..., selected: bool = ...
    ) -> Option: ...

class OptionGroup(Element):
    label: Optional[str]
    disabled: bool
    def __init__(self, label: str) -> None: ...
    def create_option(
        self, label: str, value: Optional[str] = ...
    ) -> Option: ...

class Option(Element):
    value: Optional[str]
    disabled: bool
    selected: bool
    def __init__(self, label: str, value: Optional[str] = None) -> None: ...

class Label(Element):
    for_: Optional[str]
    def __init__(self, *children: Union[str, bytes, Generator]) -> None: ...
