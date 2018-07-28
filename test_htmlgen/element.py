import re
from unittest import TestCase

from asserts import (assert_false, assert_true, assert_equal, assert_is_none,
                     assert_raises)

from htmlgen.element import Element, VoidElement, NonVoidElement


class NonVoidElementTest(TestCase):

    def test_generate_children(self):
        class TestingElement(NonVoidElement):
            def generate_children(self):
                yield "Hello World!"
                yield VoidElement("br")
        element = TestingElement("div")
        assert_equal([b"<div>", b"Hello World!", b"<br/>", b"</div>"],
                     list(iter(element)))


# Some lines below are marked "type: ignore".
# See https://github.com/python/mypy/issues/220 for details.
class ElementTest(TestCase):

    def test_true(self):
        assert_true(Element("div"))

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

    def test_attribute_order(self):
        """Test attribute order.

        The attributes are ordered alphabetically so that unit and doctests
        can rely on this order.

        """
        element = Element("div")
        element.set_attribute("def", "")
        element.set_attribute("abc", "")
        element.set_attribute("ghi", "")
        assert_equal([b'<div abc="" def="" ghi="">', b"</div>"],
                     list(iter(element)))

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

    def test_attribute_names(self):
        element = Element("div")
        element.set_attribute("foo", "")
        element.set_attribute("bar", "")
        element.remove_attribute("foo")
        assert_equal({"bar"}, element.attribute_names)

    def test_add_one_css_classes(self):
        element = Element("div")
        element.add_css_classes("foo")
        assert_equal([b'<div class="foo">', b'</div>'], list(iter(element)))

    def test_add_multiple_css_classes(self):
        element = Element("div")
        element.add_css_classes("foo", "bar", "baz")
        element.add_css_classes("bar")
        matches = re.search(r'class="(.*)"', str(element))
        assert matches is not None
        css_classes = matches.group(1).split(" ")
        assert_equal(["bar", "baz", "foo"], css_classes)

    def test_remove_css_classes(self):
        element = Element("div")
        element.add_css_classes("foo", "bar", "baz")
        element.remove_css_classes("bar", "xxx")
        matches = re.search(r'class="(.*)"', str(element))
        assert matches is not None
        css_classes = matches.group(1).split(" ")
        css_classes.sort()
        assert_equal(["baz", "foo"], css_classes)

    def test_has_css_class(self):
        element = Element("div")
        element.add_css_classes("foo")
        assert_false(element.has_css_class("bar"))
        element.add_css_classes("bar")
        assert_true(element.has_css_class("bar"))
        element.remove_css_classes("bar")
        assert_false(element.has_css_class("bar"))

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
        assert matches is not None
        css_classes = matches.group(1).split("; ")
        css_classes.sort()
        assert_equal(["background-color: rgb(255, 0, 0)",
                      "color: black",
                      "display: block"], css_classes)

    def test_id(self):
        element = Element("div")
        element.id = "Test-ID"
        assert_equal("Test-ID", element.id)
        assert_equal('<div id="Test-ID"></div>', str(element))
        element.id = ""
        assert_is_none(element.id)
        assert_equal('<div></div>', str(element))
        element.id = None
        assert_is_none(element.id)
        assert_equal('<div></div>', str(element))

    def test_id_space(self):
        element = Element("div")
        with assert_raises(ValueError):
            element.id = "Test ID"

    def test_data_set(self):
        element = Element("div")
        element.data["foo"] = "bar"
        element.data["abc-def"] = "Another Value"
        assert_equal([b'<div data-abc-def="Another Value" data-foo="bar">',
                      b"</div>"], list(iter(element)))

    def test_data_get(self):
        element = Element("div")
        element.data["foo"] = "bar"
        assert_equal("bar", element.data["foo"])

    def test_data_get_not_set(self):
        element = Element("div")
        with assert_raises(KeyError):
            element.data["foo"]

    def test_data_overwrite(self):
        element = Element("div")
        element.data["foo"] = "bar"
        element.data["foo"] = "new"
        assert_equal([b'<div data-foo="new">', b"</div>"], list(iter(element)))

    def test_data_delete(self):
        element = Element("div")
        element.data["foo"] = "bar"
        del element.data["foo"]
        assert_equal([b'<div>', b"</div>"], list(iter(element)))

    def test_data_delete_unknown(self):
        element = Element("div")
        with assert_raises(KeyError):
            del element.data["foo"]

    def test_data_clear(self):
        element = Element("div")
        element.data = {"old": "xxx", "foo": "old-value"}  # type: ignore
        element.data.clear()
        assert_equal([b'<div>', b"</div>"], list(iter(element)))

    def test_data_replace(self):
        element = Element("div")
        element.data = {"old": "xxx", "foo": "old-value"}  # type: ignore
        element.data = {"foo": "bar", "abc": "def"}  # type: ignore
        assert_equal([b'<div data-abc="def" data-foo="bar">', b"</div>"],
                     list(iter(element)))

    def test_data_iteration(self):
        element = Element("div")
        element.set_attribute("foo", "v1")
        element.set_attribute("data-bar", "v2")
        items = list(iter(element.data))
        assert_equal(["bar"], items)

    def test_data_length(self):
        element = Element("div")
        element.set_attribute("foo", "v1")
        element.set_attribute("data-bar", "v2")
        element.set_attribute("data-baz", "v3")
        assert_equal(2, len(element.data))

    def test_data_external(self):
        element = Element("div")
        element.set_attribute("data-foo", "bar")
        assert_equal("bar", element.data["foo"])
        element.data["xyz"] = "abc"
        assert_equal("abc", element.get_attribute("data-xyz"))
        element.data.clear()
        assert_is_none(element.get_attribute("data-foo"))
        element.set_attribute("data-old", "")
        element.data = {}  # type: ignore
        assert_is_none(element.get_attribute("data-old"))


class ShortElementTest(TestCase):

    def test_empty(self):
        element = VoidElement("br")
        assert_equal([b'<br/>'], list(iter(element)))

    def test_attribute(self):
        element = VoidElement("br")
        element.set_attribute("data-foo", "bar")
        assert_equal([b'<br data-foo="bar"/>'], list(iter(element)))
