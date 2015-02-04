import datetime
import re

from htmlgen.attribute import (html_attribute, boolean_html_attribute,
                               int_html_attribute, float_html_attribute)
from htmlgen.block import Division
from htmlgen.element import Element, VoidElement


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
    encryption_type = html_attribute("enctype", _ENC_TYPE_URL_ENCODED)

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

    def __init__(self, name=None, value=""):
        """Create an HTML text input element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        The value argument determines the initial content of the text field.

        """
        super(TextInput, self).__init__("text", name)
        self.value = value


class PasswordInput(Input):

    """An HTML password input (<input type="password">) element."""

    def __init__(self, name=None):
        """Create an HTML password input element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        """
        super(PasswordInput, self).__init__("password", name)


class NumberInput(Input):

    """An HTML number input (<input type="number">) element."""

    def __init__(self, name=None, value=None):
        """Create an HTML number input element.

        The optional name argument sets this input element's name, used when
        submitting a form.

        If value is not None, it determines the initial content of the
        number field.

        """
        super(NumberInput, self).__init__("number", name)
        if value is not None:
            self.value = str(value)

    minimum = float_html_attribute("min")
    maximum = float_html_attribute("max")
    step = float_html_attribute("step")


class DateInput(Input):

    """An HTML date input (<input type="date">) element."""

    def __init__(self, name=None, date=None):
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
