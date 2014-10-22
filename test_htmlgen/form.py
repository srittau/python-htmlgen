import datetime
from unittest import TestCase

from asserts import assert_equal, assert_is_none

from htmlgen.form import (Form, Input, TextInput, SubmitButton, Button,
                          NumberInput, PasswordInput, DateInput)


class FormTest(TestCase):

    def test_implicit_arguments(self):
        form = Form("PUT", "/test")
        assert_equal("PUT", form.method)
        assert_equal("/test", form.url)
        assert_equal([b'<form action="/test" method="PUT">', b"</form>"],
                     list(iter(form)))

    def test_default_arguments(self):
        form = Form()
        assert_equal("POST", form.method)
        assert_equal("", form.url)
        assert_equal([b'<form>', b"</form>"], list(iter(form)))


class InputTest(TestCase):

    def test_with_name(self):
        input_ = Input("number", "my-name")
        assert_equal("number", input_.type)
        assert_equal("my-name", input_.name)
        assert_equal("", input_.value)
        assert_equal([b'<input name="my-name" type="number"/>'],
                     list(iter(input_)))

    def test_defaults(self):
        input_ = Input()
        assert_equal("text", input_.type)
        assert_equal("", input_.name)
        assert_equal([b'<input type="text"/>'], list(iter(input_)))

    def test_attributes(self):
        input_ = Input()
        input_.placeholder = "Foo"
        input_.size = 5
        input_.value = "My Value"
        assert_equal([b'<input placeholder="Foo" size="5" type="text" '
                      b'value="My Value"/>'],
                     list(iter(input_)))

    def test_boolean_attributes(self):
        input_ = Input()
        input_.disabled = True
        input_.focus = True
        input_.readonly = True
        assert_equal([b'<input autofocus="autofocus" disabled="disabled" '
                      b'readonly="readonly" type="text"/>'],
                     list(iter(input_)))


class TextInputTest(TestCase):

    def test_defaults(self):
        input_ = TextInput()
        assert_equal("text", input_.type)
        assert_equal("", input_.name)
        assert_equal("", input_.value)
        assert_equal([b'<input type="text"/>'],
                     list(iter(input_)))

    def test_with_arguments(self):
        input_ = TextInput("my-text", "Default Value")
        assert_equal("my-text", input_.name)
        assert_equal("Default Value", input_.value)
        assert_equal([b'<input name="my-text" type="text" '
                      b'value="Default Value"/>'],
                     list(iter(input_)))


class PasswordInputTest(TestCase):

    def test_defaults(self):
        input_ = PasswordInput()
        assert_equal("password", input_.type)
        assert_equal("", input_.name)
        assert_equal("", input_.value)
        assert_equal([b'<input type="password"/>'],
                     list(iter(input_)))

    def test_with_arguments(self):
        input_ = PasswordInput("my-pw")
        assert_equal("my-pw", input_.name)
        assert_equal([b'<input name="my-pw" type="password"/>'],
                     list(iter(input_)))


class NumberInputTest(TestCase):

    def test_defaults(self):
        number = NumberInput()
        assert_equal("number", number.type)
        assert_equal("", number.name)
        assert_equal("", number.value)
        assert_equal('<input type="number"/>', str(number))

    def test_with_arguments(self):
        number = NumberInput("my-number", 3.4)
        assert_equal("my-number", number.name)
        assert_equal("3.4", number.value)
        assert_equal('<input name="my-number" type="number" value="3.4"/>',
                     str(number))

    def test_value_zero(self):
        number = NumberInput(value=0)
        assert_equal("0", number.value)
        assert_equal('<input type="number" value="0"/>', str(number))

    def test_attributes(self):
        number = NumberInput()
        number.minimum = 4.1
        number.maximum = 10.5
        number.step = 0.8
        assert_equal('<input max="10.5" min="4.1" step="0.8" type="number"/>',
                     str(number))


class DateInputTest(TestCase):

    def test_defaults(self):
        input_ = DateInput()
        assert_equal("date", input_.type)
        assert_equal("", input_.name)
        assert_is_none(input_.date)
        assert_equal("", input_.value)
        assert_equal('<input type="date"/>', str(input_))

    def test_with_arguments(self):
        input_ = DateInput("my-date", datetime.date(2014, 3, 22))
        assert_equal("my-date", input_.name)
        assert_equal(datetime.date(2014, 3, 22), input_.date)
        assert_equal("2014-03-22", input_.value)
        assert_equal('<input name="my-date" type="date" value="2014-03-22"/>',
                     str(input_))

    def test_value(self):
        input_ = DateInput()
        input_.value = "2012-03-08"
        assert_equal(datetime.date(2012, 3, 8), input_.date)
        input_.value = "invalid"
        assert_is_none(input_.date)
        assert_equal('<input type="date" value="invalid"/>', str(input_))
        input_.date = None
        assert_equal("", input_.value)
        assert_equal('<input type="date"/>', str(input_))


class SubmitButtonTest(TestCase):
    
    def test_construct(self):
        button = SubmitButton("My Label")
        assert_equal("My Label", button.label)
        assert_equal("My Label", button.value)
        assert_equal([b'<input type="submit" value="My Label"/>'],
                     list(iter(button)))

    def test_label(self):
        button = SubmitButton("")
        button.label = "My Label"
        assert_equal("My Label", button.label)
        assert_equal("My Label", button.value)
        button.value = "New Label"
        assert_equal("New Label", button.label)
        assert_equal("New Label", button.value)


class ButtonTest(TestCase):

    def test_with_children(self):
        button = Button("Foo", "bar")
        assert_equal("<button>Foobar</button>", str(button))
