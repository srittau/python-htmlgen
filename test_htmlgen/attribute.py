from unittest import TestCase

from asserts import assert_true, assert_false, assert_is_none, assert_equal

from htmlgen.attribute import (html_attribute,
                               boolean_html_attribute,
                               int_html_attribute,
                               float_html_attribute)
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
