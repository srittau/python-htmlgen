import datetime
from unittest import TestCase

from asserts import assert_true, assert_false, assert_is_none, assert_equal

from htmlgen.attribute import (html_attribute,
                               boolean_html_attribute,
                               int_html_attribute,
                               float_html_attribute,
                               time_html_attribute,
                               list_html_attribute, data_attribute,
                               css_class_attribute)
from htmlgen.element import Element


class HTMLAttributeTest(TestCase):

    def test_regular(self):
        class MyElement(Element):
            attr = html_attribute("data-attr")
        element = MyElement("div")
        assert_is_none(element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = "Foo"
        assert_equal("Foo", element.attr)
        assert_equal('<div data-attr="Foo"></div>', str(element))
        element.attr = None
        assert_is_none(element.attr)
        assert_equal("<div></div>", str(element))

    def test_regular_with_default(self):
        class MyElement(Element):
            attr = html_attribute("data-attr", default="Bar")
        element = MyElement("div")
        assert_equal("Bar", element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = "Foo"
        assert_equal("Foo", element.attr)
        assert_equal('<div data-attr="Foo"></div>', str(element))
        element.attr = "Bar"
        assert_equal("Bar", element.attr)
        assert_equal('<div></div>', str(element))
        element.attr = None
        assert_equal("Bar", element.attr)
        assert_equal('<div></div>', str(element))

    def test_boolean(self):
        class MyElement(Element):
            attr = boolean_html_attribute("data-attr")
        element = MyElement("div")
        assert_false(element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = True
        assert_true(element.attr)
        assert_equal('<div data-attr="data-attr"></div>', str(element))
        element.attr = False
        assert_false(element.attr)
        assert_equal('<div></div>', str(element))

    def test_integer(self):
        class MyElement(Element):
            attr = int_html_attribute("data-attr")
        element = MyElement("div")
        assert_is_none(element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = 42
        assert_equal(42, element.attr)
        assert_equal('<div data-attr="42"></div>', str(element))
        element.attr = None
        assert_is_none(element.attr)
        assert_equal('<div></div>', str(element))

    def test_integer_with_default(self):
        class MyElement(Element):
            attr = int_html_attribute("data-attr", default=42)
        element = MyElement("div")
        assert_equal(42, element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = 4711
        assert_equal(4711, element.attr)
        assert_equal('<div data-attr="4711"></div>', str(element))
        element.attr = 42
        assert_equal(42, element.attr)
        assert_equal('<div></div>', str(element))
        element.attr = None
        assert_equal(42, element.attr)
        assert_equal('<div></div>', str(element))

    def test_float(self):
        class MyElement(Element):
            attr = float_html_attribute("data-attr")
        element = MyElement("div")
        assert_is_none(element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = 4.2
        assert_equal(4.2, element.attr)
        assert_equal('<div data-attr="4.2"></div>', str(element))
        element.attr = None
        assert_is_none(element.attr)
        assert_equal('<div></div>', str(element))

    def test_float_with_default(self):
        class MyElement(Element):
            attr = float_html_attribute("data-attr", default=4.2)
        element = MyElement("div")
        assert_equal(4.2, element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = 47.11
        assert_equal(47.11, element.attr)
        assert_equal('<div data-attr="47.11"></div>', str(element))
        element.attr = 4.2
        assert_equal(4.2, element.attr)
        assert_equal('<div></div>', str(element))
        element.attr = None
        assert_equal(4.2, element.attr)
        assert_equal('<div></div>', str(element))

    def test_time(self):
        class MyElement(Element):
            attr = time_html_attribute("data-time")
        element = MyElement("div")
        assert_is_none(element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = datetime.time(14, 13, 9)
        assert_equal(datetime.time(14, 13, 9), element.attr)
        assert_equal('<div data-time="14:13:09"></div>', str(element))
        element.attr = None
        assert_is_none(element.attr)
        assert_equal('<div></div>', str(element))
        element.set_attribute("data-time", "09:33:04")
        assert_equal(datetime.time(9, 33, 4), element.attr)

    def test_time_with_fraction(self):
        class MyElement(Element):
            attr = time_html_attribute("data-time")
        element = MyElement("div")
        element.attr = datetime.time(14, 13, 9, 123456)
        assert_equal(datetime.time(14, 13, 9, 123456), element.attr)
        assert_equal('<div data-time="14:13:09.123456"></div>', str(element))

    def test_time__invalid_value(self):
        class MyElement(Element):
            attr = time_html_attribute("data-time")
        element = MyElement("div")
        element.set_attribute("data-time", "INVALID")
        assert_is_none(element.attr)

    def test_time_with_default(self):
        class MyElement(Element):
            attr = time_html_attribute(
                "data-attr", default=datetime.time(12, 9, 34))
        element = MyElement("div")
        assert_equal(datetime.time(12, 9, 34), element.attr)
        assert_equal("<div></div>", str(element))
        element.attr = datetime.time(12, 9, 34)
        assert_equal(datetime.time(12, 9, 34), element.attr)
        assert_equal("<div></div>", str(element))

    def test_list(self):
        class MyElement(Element):
            attr = list_html_attribute("data-attr")
        element = MyElement("div")
        assert_equal([], element.attr)
        element.set_attribute("data-attr", "")
        assert_equal([], element.attr)
        element.set_attribute("data-attr", "foo,bar")
        assert_equal(["foo", "bar"], element.attr)
        element.attr = []
        assert_equal('<div></div>', str(element))
        element.attr = ["abc", "def"]
        assert_equal(["abc", "def"], element.attr)
        element.attr.append("ghi")
        assert_equal(["abc", "def"], element.attr)
        assert_equal("abc,def", element.get_attribute("data-attr"))
        assert_equal('<div data-attr="abc,def"></div>', str(element))

    def test_data(self):
        class MyElement(Element):
            attr = data_attribute("attr")
        element = MyElement("div")
        assert_is_none(element.get_attribute("data-attr"))
        element.attr = "foo"
        assert_equal("foo", element.get_attribute("data-attr"))
        element.set_attribute("data-attr", "bar")
        assert_equal("bar", element.attr)

    def test_data_with_default(self):
        class MyElement(Element):
            attr = data_attribute("attr", "def")
        element = MyElement("div")
        element.attr = "def"
        assert_is_none(element.get_attribute("data-attr"))

    def test_css_class(self):
        class MyElement(Element):
            attr = css_class_attribute("my-class")
        element = MyElement("div")
        assert_false(element.attr)
        element.add_css_classes("other-class")
        assert_false(element.attr)
        element.add_css_classes("my-class")
        assert_true(element.attr)
        element.attr = False
        assert_false(element.has_css_class("my-class"))
        element.attr = False
        assert_false(element.has_css_class("my-class"))
        element.attr = True
        assert_true(element.has_css_class("my-class"))
        element.attr = True
        assert_true(element.has_css_class("my-class"))
