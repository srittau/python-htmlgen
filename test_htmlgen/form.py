import datetime
from unittest import TestCase

from asserts import (assert_false, assert_true,
                     assert_is_none,
                     assert_equal, assert_is,
                     assert_raises)

from htmlgen import (
    Span, Form, Input, TextInput, SubmitButton, Button,
    NumberInput, SearchInput, PasswordInput, DateInput, TimeInput, FileInput,
    Checkbox, RadioButton, TextArea, Select, OptionGroup, Option, Label)


class FormTest(TestCase):

    def test_implicit_arguments(self):
        form = Form("PUT", "/test")
        assert_equal("PUT", form.method)
        assert_equal("/test", form.url)
        assert_equal("_self", form.target)
        assert_equal([b'<form action="/test" method="PUT">', b"</form>"],
                     list(iter(form)))

    def test_default_arguments(self):
        form = Form()
        assert_equal("GET", form.method)
        assert_equal("", form.url)
        assert_equal([b'<form>', b"</form>"], list(iter(form)))

    def test_target(self):
        form = Form()
        form.target = "my-target"
        assert_equal('<form target="my-target"></form>', str(form))
        form.set_blank_target()
        assert_equal("_blank", form.target)
        assert_equal('<form target="_blank"></form>', str(form))

    def test_multipart(self):
        form = Form()
        assert_false(form.multipart)
        assert_equal("application/x-www-form-urlencoded", form.encryption_type)
        form.multipart = True
        assert_equal("multipart/form-data", form.encryption_type)
        form.multipart = False
        assert_equal("application/x-www-form-urlencoded", form.encryption_type)
        form.encryption_type = "multipart/form-data"
        assert_true(form.multipart)
        form.encryption_type = "application/x-www-form-urlencoded"
        assert_false(form.multipart)


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


class SearchInputTest(TestCase):

    def test_defaults(self):
        search = SearchInput()
        assert_equal("search", search.type)
        assert_equal("", search.name)
        assert_equal("", search.value)
        assert_equal('<input type="search"/>', str(search))

    def test_with_arguments(self):
        search = SearchInput("my-search")
        assert_equal("my-search", search.name)
        assert_equal('<input name="my-search" type="search"/>', str(search))


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
        assert_is_none(number.number)
        assert_equal('<input type="number"/>', str(number))

    def test_with_arguments(self):
        number = NumberInput("my-number", 3.4)
        assert_equal("my-number", number.name)
        assert_equal("3.4", number.value)
        assert_equal(3.4, number.number)
        assert_equal('<input name="my-number" type="number" value="3.4"/>',
                     str(number))

    def test_value_zero(self):
        number = NumberInput(number=0)
        assert_equal("0", number.value)
        assert_equal(0, number.number)
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


class TimeInputTest(TestCase):

    def test_defaults(self):
        time = TimeInput()
        assert_equal("", time.name)
        assert_is_none(time.time)
        assert_is_none(time.minimum)
        assert_is_none(time.maximum)
        assert_is_none(time.step)
        assert_equal('<input type="time"/>', str(time))

    def test_construct_with_arguments(self):
        time = TimeInput("time-name", datetime.time(14, 30, 12))
        assert_equal("time-name", time.name)
        assert_equal(datetime.time(14, 30, 12), time.time)
        assert_equal('<input name="time-name" type="time" '
                     'value="14:30:12"/>', str(time))

    def test_minimum_maximum(self):
        time = TimeInput()
        time.minimum = datetime.time(12, 14)
        time.maximum = datetime.time(19, 45)
        assert_equal('<input max="19:45:00" min="12:14:00" type="time"/>',
                     str(time))
        time.minimum = None
        time.maximum = None
        assert_equal('<input type="time"/>', str(time))

    def test_minimum_above_maximum(self):
        time = TimeInput()
        time.maximum = datetime.time(12, 0)
        with assert_raises(ValueError):
            time.minimum = datetime.time(12, 1)

    def test_maximum_below_minimum(self):
        time = TimeInput()
        time.minimum = datetime.time(12, 1)
        with assert_raises(ValueError):
            time.maximum = datetime.time(12, 0)

    def test_step(self):
        time = TimeInput()
        time.step = 12.3
        assert_equal(12.3, time.step)
        assert_equal('<input step="12.3" type="time"/>', str(time))
        time.step = None
        assert_is_none(time.step)
        assert_equal('<input type="time"/>', str(time))
        time.set_attribute("step", "any")
        assert_is_none(time.step)

    def test_step_get_invalid(self):
        time = TimeInput()
        time.set_attribute("step", "invalid")
        assert_is_none(time.step)
        time.set_attribute("step", "0")
        assert_is_none(time.step)
        time.set_attribute("step", "-1")
        assert_is_none(time.step)

    def test_step_set_invalid(self):
        time = TimeInput()
        with assert_raises(ValueError):
            time.step = 0


class CheckboxTest(TestCase):

    def test_defaults(self):
        checkbox = Checkbox()
        assert_equal("checkbox", checkbox.type)
        assert_equal("", checkbox.name)
        assert_equal("", checkbox.value)
        assert_false(checkbox.checked)
        assert_equal('<input type="checkbox"/>', str(checkbox))

    def test_name_and_value(self):
        checkbox = Checkbox("my-name", "my-value")
        assert_equal("my-name", checkbox.name)
        assert_equal("my-value", checkbox.value)
        assert_equal(
            '<input name="my-name" type="checkbox" value="my-value"/>',
            str(checkbox))

    def test_checked(self):
        checkbox = Checkbox()
        checkbox.checked = True
        assert_true(checkbox.checked)
        assert_equal(
            '<input checked="checked" type="checkbox"/>', str(checkbox))


class RadioButtonTest(TestCase):

    def test_defaults(self):
        radio = RadioButton()
        assert_equal("radio", radio.type)
        assert_equal("", radio.name)
        assert_equal("", radio.value)
        assert_false(radio.checked)
        assert_equal('<input type="radio"/>', str(radio))

    def test_name_and_value(self):
        radio = RadioButton("my-name", "my-value")
        assert_equal("my-name", radio.name)
        assert_equal("my-value", radio.value)
        assert_equal(
            '<input name="my-name" type="radio" value="my-value"/>',
            str(radio))

    def test_checked(self):
        radio = RadioButton()
        radio.checked = True
        assert_true(radio.checked)
        assert_equal(
            '<input checked="checked" type="radio"/>', str(radio))


class FileInputTest(TestCase):

    def test_defaults(self):
        file_input = FileInput()
        assert_equal("", file_input.name)
        assert_is_none(file_input.max_length)
        assert_equal('<input type="file"/>', str(file_input))

    def test_construct_with_name(self):
        file_input = FileInput("file-name")
        assert_equal("file-name", file_input.name)
        assert_equal('<input name="file-name" type="file"/>', str(file_input))

    def test_max_length(self):
        file_input = FileInput()
        file_input.max_length = 10000
        assert_equal('<input maxlength="10000" type="file"/>', str(file_input))

    def test_accepts(self):
        file_input = FileInput()
        assert_equal([], file_input.accept)
        file_input.set_attribute("accept", "")
        assert_equal([], file_input.accept)
        file_input.set_attribute("accept", "audio/*,image/*")
        assert_equal(["audio/*", "image/*"], file_input.accept)
        file_input.accept = ["image/png", "image/jpeg"]
        file_input.accept.append("image/gif")
        assert_equal(["image/png", "image/jpeg"], file_input.accept)
        assert_equal(
            "image/png,image/jpeg", file_input.get_attribute("accept"))
        assert_equal('<input accept="image/png,image/jpeg" type="file"/>',
                     str(file_input))


class HiddenInputTest(TestCase):

    def test_construct(self):
        button = SubmitButton("My Label")
        assert_equal("My Label", button.label)
        assert_equal("My Label", button.value)
        assert_equal([b'<input type="submit" value="My Label"/>'],
                     list(iter(button)))


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


class TextAreaTest(TestCase):

    def test_with_name(self):
        text_area = TextArea("my-name")
        assert_equal('<textarea name="my-name"></textarea>', str(text_area))

    def test_without_name(self):
        text_area = TextArea()
        assert_equal('<textarea></textarea>', str(text_area))


class SelectTest(TestCase):

    def test_attributes(self):
        select = Select()
        assert_false(select.disabled)

    def test_with_name(self):
        select = Select("my-name")
        assert_equal("my-name", select.name)
        assert_equal('<select name="my-name"></select>', str(select))

    def test_without_name(self):
        select = Select()
        assert_equal("", select.name)
        assert_equal('<select></select>', str(select))

    def test_create_group(self):
        select = Select()
        group = select.create_group("Group Label")
        assert_equal("Group Label", group.label)
        assert_equal('<select><optgroup label="Group Label"></optgroup>'
                     '</select>', str(select))

    def test_create_option(self):
        select = Select()
        select.create_option("Option Label")
        assert_equal('<select><option>Option Label</option></select>',
                     str(select))

    def test_create_option__selected(self):
        select = Select()
        option = select.create_option("Option Label", "test-value",
                                      selected=True)
        assert_is(option, select.selected_option)
        assert_equal(
            '<select><option selected="selected" value="test-value">'
            'Option Label</option></select>',
            str(select))

    def test_create_option__option_object(self):
        select = Select()
        option = select.create_option("Option Label", "test-value",
                                      selected=True)
        assert_equal("option", option.element_name)
        assert_equal("test-value", option.value)
        assert_true(option.selected)

    def test_create_option__option_object__default_value(self):
        select = Select()
        option = select.create_option("Option Label")
        assert_equal("Option Label", option.value)

    def test_create_option__selected_deselect_others(self):
        select = Select()
        option = select.create_option("L1", selected=True)
        select.create_option("L2", selected=True)
        assert_false(option.selected)

    def test_get_selected_option(self):
        select = Select()
        select.create_option("L1", "v1")
        option = select.create_option("L2", "v2", selected=True)
        select.create_option("L3", "v3")
        assert_is(option, select.selected_option)

    def test_get_selected_option__return_first(self):
        select = Select()
        option1 = Option("L1")
        option1.selected = True
        option2 = Option("L2")
        option2.selected = True
        select.append(option1)
        select.append(option2)
        assert_is(option1, select.selected_option)

    def test_get_selected_option__no_selected_elements(self):
        select = Select()
        select.create_option("L1", "v1")
        select.create_option("L2", "v2")
        select.create_option("L3", "v3")
        assert_is_none(select.selected_option)

    def test_get_selected_option__non_option_elements(self):
        select = Select()
        select.append("String Content")
        assert_is_none(select.selected_option)

    def test_get_selected_option__in_option_group(self):
        select = Select()
        group = select.create_group("")
        option = group.create_option("")
        option.selected = True
        assert_is(option, select.selected_option)

    def test_get_selected_option__option_group_has_string_child(self):
        select = Select()
        group = select.create_group("")
        group.append("XXX")
        assert_is_none(select.selected_option)

    def test_set_selected_option(self):
        select = Select()
        select.create_option("L1")
        option = select.create_option("L2")
        select.create_option("L3")
        select.selected_option = option
        assert_true(option.selected)
        assert_is(option, select.selected_option)

    def test_set_selected_option__deselect_others(self):
        select = Select()
        option1 = select.create_option("L1", selected=True)
        option2 = select.create_option("L2")
        select.selected_option = option2
        assert_false(option1.selected)
        assert_is(option2, select.selected_option)

    def test_set_selected_option__string_children(self):
        select = Select()
        select.append("String Content")
        option = select.create_option("L1")
        select.selected_option = option

    def test_get_selected_value(self):
        select = Select()
        select.create_option("L1", "v1")
        select.create_option("L2", "v2", selected=True)
        assert_equal("v2", select.selected_value)

    def test_get_selected_value__implicit_value(self):
        select = Select()
        select.create_option("L1")
        select.create_option("L2", selected=True)
        assert_equal("L2", select.selected_value)

    def test_get_selected_value__no_selected(self):
        select = Select()
        select.create_option("L1", "v1")
        assert_is_none(select.selected_value)

    def test_set_selected_value(self):
        select = Select()
        select.create_option("L1", "v1")
        option = select.create_option("L2", "v2")
        select.create_option("L3", "v3")
        select.selected_value = "v2"
        assert_equal("v2", select.selected_value)
        assert_is(option, select.selected_option)
        assert_true(option.selected)

    def test_set_selected_value__value_not_found(self):
        select = Select()
        select.create_option("L1", "v1")
        select.create_option("L2", "v2")
        with assert_raises(ValueError):
            select.selected_value = "not-found"


class OptionGroupTest(TestCase):

    def test_default(self):
        group = OptionGroup("Test Label")
        assert_equal("Test Label", group.label)
        assert_false(group.disabled)
        assert_equal('<optgroup label="Test Label"></optgroup>', str(group))

    def test_disabled(self):
        group = OptionGroup("Test Label")
        group.disabled = True
        assert_equal('<optgroup disabled="disabled" label="Test Label">'
                     '</optgroup>', str(group))

    def create_option(self):
        group = OptionGroup("")
        group.create_option("Option Label")
        assert_equal('<optgroup label=""><option>Option Label'
                     '</option></optgroup>', str(group))


class OptionTest(TestCase):

    def test_default_value(self):
        option = Option("Test Label")
        assert_equal("Test Label", option.value)
        assert_equal('<option>Test Label</option>', str(option))
        assert_false(option.selected)
        assert_false(option.disabled)

    def test_with_value(self):
        option = Option("Test Label", "test-value")
        assert_equal("test-value", option.value)
        assert_equal('<option value="test-value">Test Label</option>',
                     str(option))

    def test_set_value(self):
        option = Option("Test Label")
        option.value = "test-value"
        assert_equal("test-value", option.value)
        assert_equal('<option value="test-value">Test Label</option>',
                     str(option))

    def test_set_value_to_none(self):
        option = Option("Test Label", "test-value")
        option.value = None
        assert_equal("Test Label", option.value)
        assert_equal('<option>Test Label</option>', str(option))


class LabelTest(TestCase):

    def test_default(self):
        label = Label()
        assert_equal('<label></label>', str(label))

    def test_children(self):
        label = Label("Foo", Span())
        assert_equal('<label>Foo<span></span></label>', str(label))

    def test_for(self):
        label = Label()
        assert_is_none(label.for_)
        label.for_ = "my-id"
        assert_equal("my-id", label.for_)
        assert_equal('<label for="my-id"></label>', str(label))
