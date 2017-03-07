import datetime
import re

from htmlgen.attribute import (html_attribute, boolean_html_attribute,
                               int_html_attribute, float_html_attribute,
                               time_html_attribute, list_html_attribute)
from htmlgen.block import Division
from htmlgen.element import Element, VoidElement, is_element
from htmlgen.timeutil import parse_rfc3339_partial_time


_ENC_TYPE_URL_ENCODED = "application/x-www-form-urlencoded"
_ENC_TYPE_MULTI_PART = "multipart/form-data"


class Form(Element):

    """An HTML <form> element.

        >>> form = Form("POST", "/feedback")
        >>> form.append(Division("Name: ", TextInput("name")))
        >>> form.append(Division(SubmitButton("Submit")))

    If the form contains file input elements, set multipart to True:

        >>> form.multipart = True
        >>> form.encryption_type
        'multipart/form-data'

    """

    def __init__(self, method="GET", url=""):
        super(Form, self).__init__("form")
        self.method = method
        self.url = url

    method = html_attribute("method", default="GET")
    url = html_attribute("action", default="")
    target = html_attribute("target", "_self")
    encryption_type = html_attribute("enctype", _ENC_TYPE_URL_ENCODED)

    def set_blank_target(self):
        self.target = "_blank"

    @property
    def multipart(self):
        return self.encryption_type == _ENC_TYPE_MULTI_PART

    @multipart.setter
    def multipart(self, multipart):
        if multipart:
            self.encryption_type = _ENC_TYPE_MULTI_PART
        else:
            self.encryption_type = _ENC_TYPE_URL_ENCODED


class Input(VoidElement):

    """An HTML <input> element.

        >>> input_ = Input("text", "description")
        >>> input_.size = 20
        >>> input_.placeholder = "Enter description..."

    For most input types, a specific sub-class is provided.

    """

    def __init__(self, type_="text", name=""):
        """Create an HTML input element.

        The type_ argument sets the HTML type attribute. Possible values are
        'text', 'email', 'password', 'submit', etc. For most of these types,
        a more specific sub-class is provided.

        The optional name argument sets this input element's name, used when
        submitting a form.

        """
        super(Input, self).__init__("input")
        self.type = type_
        self.name = name

    name = html_attribute("name", default="")
    value = html_attribute("value", default="")
    readonly = boolean_html_attribute("readonly")
    disabled = boolean_html_attribute("disabled")
    type = html_attribute("type")
    placeholder = html_attribute("placeholder")
    size = int_html_attribute("size")
    focus = boolean_html_attribute("autofocus")


class TextInput(Input):

    """An HTML text input (<input type="text">) element.

        >>> input_ = TextInput("description")
        >>> input_.size = 20
        >>> input_.placeholder = "Enter description..."
        >>> input_.value = "Current Text"

    """

    def __init__(self, name="", value=""):
        """Create an HTML text input element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        The value argument determines the initial content of the text field.

        """
        super(TextInput, self).__init__("text", name)
        self.value = value


class SearchInput(Input):

    """An HTML search (<input type="search">) element."""

    def __init__(self, name=""):
        """Create an HTML search element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        """
        super(SearchInput, self).__init__("search", name)


class PasswordInput(Input):

    """An HTML password input (<input type="password">) element."""

    def __init__(self, name=""):
        """Create an HTML password input element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        """
        super(PasswordInput, self).__init__("password", name)


class NumberInput(Input):

    """An HTML number input (<input type="number">) element."""

    def __init__(self, name="", number=None):
        """Create an HTML number input element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        If number is not None, it determines the initial content of the
        this input element.

        """
        super(NumberInput, self).__init__("number", name)
        if number is not None:
            self.number = number

    number = float_html_attribute("value")
    minimum = float_html_attribute("min")
    maximum = float_html_attribute("max")
    step = float_html_attribute("step")


class DateInput(Input):

    """An HTML date input (<input type="date">) element."""

    def __init__(self, name="", date=None):
        """Create an HTML date element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        date is the initial date. If date is None, the field is initially
        empty.

        """
        super(DateInput, self).__init__("date", name)
        self.date = date

    @property
    def date(self):
        """Return the element's value attribute, parsed as date.

        If value is empty or can not be parsed as a date, return None.

        """
        return self._parse_date(self.value)

    @date.setter
    def date(self, date):
        """Set the element's value to the given date. If date is None,
        clear the value."""
        self.value = date.strftime("%Y-%m-%d") if date else ""

    @staticmethod
    def _parse_date(v):
        match = re.match(r"(\d\d\d\d)-(\d\d)-(\d\d)", v)
        if not match:
            return None
        return datetime.date(int(match.group(1)), int(match.group(2)),
                             int(match.group(3)))


class TimeInput(Input):

    """An HTML time input (<input type="time">) element."""

    def __init__(self, name="", time=None):
        """Create an HTML time element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        time is the initial time. If time is None, the field is initially
        empty.

        """
        super(TimeInput, self).__init__("time", name)
        self.time = time

    time = time_html_attribute("value")

    @property
    def minimum(self):
        value = self.get_attribute("min")
        if value is None:
            return None
        return parse_rfc3339_partial_time(value)

    @minimum.setter
    def minimum(self, minimum):
        if minimum is None:
            self.remove_attribute("min")
        else:
            if self.maximum is not None and minimum > self.maximum:
                raise ValueError("minimum value is greater than maximum")
            self.set_attribute("min", str(minimum))

    @property
    def maximum(self):
        value = self.get_attribute("max")
        if value is None:
            return None
        return parse_rfc3339_partial_time(value)

    @maximum.setter
    def maximum(self, maximum):
        if maximum is None:
            self.remove_attribute("max")
        else:
            if self.minimum is not None and maximum < self.minimum:
                raise ValueError("maximum value is lower than minimum")
            self.set_attribute("max", str(maximum))

    @property
    def step(self):
        try:
            value = float(self.get_attribute("step"))
        except (TypeError, ValueError):
            return None
        if value <= 0:
            return None
        else:
            return value

    @step.setter
    def step(self, step):
        if step is None:
            self.remove_attribute("step")
        elif step <= 0:
            raise ValueError("step values must be positive numbers")
        else:
            self.set_attribute("step", str(step))


class _CheckableInput(Input):

    def __init__(self, type_, name, value):
        super(_CheckableInput, self).__init__(type_, name)
        if value:
            self.value = value

    checked = boolean_html_attribute("checked")


class Checkbox(_CheckableInput):

    """An HTML checkbox (<input type="checkbox">) element.

    >>> cb = Checkbox("my-name", "my-value")
    >>> cb.checked = True

    """

    def __init__(self, name="", value=""):
        super(Checkbox, self).__init__("checkbox", name, value)


class RadioButton(_CheckableInput):

    """An HTML radio button (<input type="radio">) element.

    >>> cb = RadioButton("my-name", "my-value")
    >>> cb.checked = True

    """

    def __init__(self, name="", value=""):
        super(RadioButton, self).__init__("radio", name, value)


class FileInput(Input):

    """An HTML file input (<input type="file">) element."""

    def __init__(self, name=""):
        super(FileInput, self).__init__("file", name)

    max_length = int_html_attribute("maxlength")
    accept = list_html_attribute("accept")


class HiddenInput(Input):

    """A hidden HTML input (<input type="hidden"/>) element."""

    def __init__(self, name, value):
        super(HiddenInput, self).__init__("hidden", name)
        self.value = value


class SubmitButton(Input):

    """An HTML form submit button (<input type="submit">) element.

        >>> button = SubmitButton("My Label")
        >>> button.label
        'My Label'

    label is an alias for value:

        >>> button.value
        'My Label'

    """

    def __init__(self, label):
        super(SubmitButton, self).__init__("submit")
        self.value = label

    @property
    def label(self):
        return self.value

    @label.setter
    def label(self, label):
        self.value = label


class Button(Element):

    """An HTML <button> element.

        >>> button = Button("My Label")

    """

    def __init__(self, *content):
        super(Button, self).__init__("button")
        self.extend(content)


class TextArea(Element):

    """An HTML <textarea> element.

        >>> area = TextArea("element-name")
        >>> area.placeholder = "Placeholder text ..."
        >>> area.append("Initial text area content.")

    """

    def __init__(self, name=""):
        super(TextArea, self).__init__("textarea")
        self.name = name

    name = html_attribute("name", default="")
    readonly = boolean_html_attribute("readonly")
    disabled = boolean_html_attribute("disabled")
    columns = int_html_attribute("cols")
    rows = int_html_attribute("rows")
    placeholder = html_attribute("placeholder")


class Select(Element):

    """An HTML selection list (<select>) element.

    >>> select = Select("element-name")
    >>> option1 = select.create_option("Option 1", "v1")
    >>> option2 = select.create_option("Option 2", "v2", selected=True)
    >>> option2 is select.selected_option
    True
    >>> option2.value == select.selected_value
    True
    >>> select.selected_value = "v1"
    >>> option1 is select.selected_option
    True

    It is also possible to use option groups:

    >>> select = Select()
    >>> group = select.create_group("Group 1")
    >>> option1 = group.create_option("Option 1")
    >>> option2 = group.create_option("Option 2")

    At the moment, multiple selection lists are not supported.

    """

    def __init__(self, name=""):
        super(Select, self).__init__("select")
        self.name = name

    name = html_attribute("name", default="")
    disabled = boolean_html_attribute("disabled")

    def create_group(self, label):
        """Create and append an option group."""
        group = OptionGroup(label)
        self.append(group)
        return group

    def create_option(self, label, value=None, selected=False):
        """Create and append an option."""
        option = Option(label, value)
        self.append(option)
        if selected:
            self.selected_option = option
        return option

    @property
    def _options_iter(self):
        for child in self.children.children:
            if is_element(child, "option"):
                yield child
            elif is_element(child, "optgroup"):
                for sub_child in child.children.children:
                    if is_element(sub_child, "option"):
                        yield sub_child

    @property
    def selected_option(self):
        """Return the first selected option object.

        If no option is selected, return None.

        """

        for child in self._options_iter:
            if child.selected:
                return child
        return None

    @selected_option.setter
    def selected_option(self, option):
        """Set the selected option object.

        All other selected options will be deselected.

        """
        for child in self._options_iter:
            child.selected = False
        option.selected = True

    @property
    def selected_value(self):
        """Return the value of the first selected option.

        If no option is selected, return None.

        """
        option = self.selected_option
        return option.value if option else None

    @selected_value.setter
    def selected_value(self, selected_value):
        """Set the selected option by its value.

        If no option has the supplied value, raise a ValueError.

        """
        for option in self._options_iter:
            if option.value == selected_value:
                self.selected_option = option
                break
        else:
            raise ValueError("no option with value '{}' found".format(
                selected_value))


class OptionGroup(Element):

    """An HTML selection list option group (<optgroup>) element.

    """

    def __init__(self, label):
        super(OptionGroup, self).__init__("optgroup")
        self.label = label

    label = html_attribute("label")
    disabled = boolean_html_attribute("disabled")

    def create_option(self, label, value=None):
        """Create and append an option."""
        option = Option(label, value)
        self.append(option)
        return option


class Option(Element):

    """An HTML selection list option (<option>) element.

    >>> option = Option("Label")
    >>> str(option)
    '<option>Label</option>'
    >>> option = Option("Label", "test-value")
    >>> str(option)
    '<option value="test-value">Label</option>'

    """

    def __init__(self, label, value=None):
        super(Option, self).__init__("option")
        self.value = value
        self.append(label)

    disabled = boolean_html_attribute("disabled")
    selected = boolean_html_attribute("selected")

    @property
    def value(self):
        """Return the value of this option.

        >>> option = Option("Label", "value")
        >>> option.value
        'value'

        If no explicit value is given, return the children as string.

        >>> option = Option("Label")
        >>> option.value
        'Label'

        """
        return self.get_attribute("value", str(self.children))

    @value.setter
    def value(self, value):
        if value is None:
            self.remove_attribute("value")
        else:
            self.set_attribute("value", value)


class Label(Element):

    """An HTML label (<label>) element.

    >>> str(Label(Checkbox(), " My Label"))
    '<label><input type="checkbox"/> My Label</label>'

    """

    def __init__(self, *children):
        super(Label, self).__init__("label")
        self.extend(children)

    for_ = html_attribute("for")
