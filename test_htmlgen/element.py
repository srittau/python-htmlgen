import re
from unittest import TestCase

from asserts import assert_false, assert_true, assert_equal, assert_is_none

from htmlgen.element import (Element,
                             html_attribute,
                             boolean_html_attribute,
                             int_html_attribute, ShortElement)


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


class ElementTest(TestCase):

    def test_append_extend(self):
        element = Element("div")
        element.append("Hello")
        element.extend([", ", "World", "!"])
        assert_equal(4, len(element))
        element.append_raw("Hello")
        element.extend_raw([", ", "World", "!"])
        assert_equal(8, len(element))

    def test_empty(self):
        element = Element("div")
        element.append("foo")
        element.empty()
        assert_equal(0, len(element))

    def test_generate_empty(self):
        element = Element("div")
        assert_equal([b"<div>", b"</div>"], list(iter(element)))

    def test_generate_with_children(self):
        element = Element("div")
        element.extend(["<foo>", "&"])
        element.append_raw("&lt;bar&gt;")
        assert_equal(
            [b"<div>", b"&lt;foo&gt;", b"&amp;", b"&lt;bar&gt;", b"</div>"],
            list(iter(element)))

    def test_attributes(self):
        element = Element("div")
        element.set_attribute("foo", "bar")
        assert_equal("bar", element.get_attribute("foo"))
        assert_equal([b'<div foo="bar">', b"</div>"], list(iter(element)))

    def test_get_attribute(self):
        element = Element("div")
        assert_is_none(element.get_attribute("foo"))
        assert_equal("XXX", element.get_attribute("foo", default="XXX"))

    def test_remove_attribute(self):
        element = Element("div")
        element.remove_attribute("foo")
        element.set_attribute("foo", "bar")
        element.remove_attribute("foo")
        assert_is_none(element.get_attribute("foo"))
        assert_equal([b'<div>', b"</div>"], list(iter(element)))

    def test_add_one_css_classes(self):
        element = Element("div")
        element.add_css_classes("foo")
        assert_equal([b'<div class="foo">', b'</div>'], list(iter(element)))

    def test_add_multiple_css_classes(self):
        element = Element("div")
        element.add_css_classes("foo", "bar", "baz")
        element.add_css_classes("bar")
        matches = re.search(r'class="(.*)"', str(element))
        css_classes = matches.group(1).split(" ")
        css_classes.sort()
        assert_equal(["bar", "baz", "foo"], css_classes)

    def test_set_one_style(self):
        element = Element("div")
        element.set_style("background-color", "rgb(255, 0, 0)")
        assert_equal([b'<div style="background-color: rgb(255, 0, 0)">',
                      b'</div>'], list(iter(element)))

    def test_set_multiple_styles(self):
        element = Element("div")
        element.set_style("color", "black")
        element.set_style("background-color", "rgb(255, 0, 0)")
        element.set_style("display", "block")
        matches = re.search(r'style="(.*)"', str(element))
        css_classes = matches.group(1).split("; ")
        css_classes.sort()
        assert_equal(["background-color: rgb(255, 0, 0)",
                      "color: black",
                      "display: block"], css_classes)


class ShortElementTest(TestCase):

    def test_empty(self):
        element = ShortElement("br")
        assert_equal([b'<br/>'], list(iter(element)))

    def test_attribute(self):
        element = ShortElement("br")
        element.set_attribute("data-foo", "bar")
        assert_equal([b'<br data-foo="bar"/>'], list(iter(element)))
