from unittest import TestCase

from asserts import assert_equal

from htmlgen.form import Form, Input, TextInput, SubmitButton


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
