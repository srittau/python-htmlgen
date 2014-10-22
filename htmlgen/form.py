from htmlgen.block import Division
from htmlgen.element import (Element, VoidElement, html_attribute,
                             boolean_html_attribute, int_html_attribute)


class Form(Element):

    """An HTML <form> element.

        >>> form = Form("POST", "/feedback")
        >>> form.append(Division("Name: ", TextInput("name")))
        >>> form.append(Division(SubmitButton("Submit")))

    """

    def __init__(self, method="POST", url=""):
        super(Form, self).__init__("form")
        self.method = method
        self.url = url

    method = html_attribute("method", default="POST")
    url = html_attribute("action", default="")


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
