from unittest import TestCase

from asserts import assert_equal

from htmlgen.list import OrderedList, UnorderedList, ListItem, DescriptionList


class OrderedListTest(TestCase):

    def test_empty(self):
        list_ = OrderedList()
        assert_equal([b"<ol>", b"</ol>"], list(iter(list_)))

    def test_create_item_no_content(self):
        list_ = OrderedList()
        item = list_.create_item()
        item.add_css_classes("test-class")
        assert_equal([b"<ol>", b'<li class="test-class">', b"</li>", b"</ol>"],
                     list(iter(list_)))

    def test_create_item_with_content(self):
        list_ = OrderedList()
        list_.create_item("Test Content")
        assert_equal([b"<ol>", b"<li>", b"Test Content", b"</li>", b"</ol>"],
                     list(iter(list_)))

    def test_create_items(self):
        list_ = OrderedList()
        items = list_.create_items("foo", "bar", "baz")
        assert_equal([b"<ol>",
                      b"<li>", b"foo", b"</li>",
                      b"<li>", b"bar", b"</li>",
                      b"<li>", b"baz", b"</li>",
                      b"</ol>"],
                     list(iter(list_)))
        assert_equal(3, len(items))

    def test_start_attribute(self):
        list_ = OrderedList()
        list_.start = 7
        assert_equal(7, list_.start)
        assert_equal([b'<ol start="7">', b"</ol>"], list(iter(list_)))

    def test_start_attribute_default(self):
        list_ = OrderedList()
        assert_equal(1, list_.start)
        list_.start = 1
        assert_equal([b'<ol>', b"</ol>"], list(iter(list_)))



class UnorderedListTest(TestCase):

    def test_empty(self):
        list_ = UnorderedList()
        assert_equal([b"<ul>", b"</ul>"], list(iter(list_)))

    def test_create_item_no_content(self):
        list_ = UnorderedList()
        item = list_.create_item()
        item.add_css_classes("test-class")
        assert_equal([b"<ul>", b'<li class="test-class">', b"</li>", b"</ul>"],
                     list(iter(list_)))

    def test_create_item_with_content(self):
        list_ = UnorderedList()
        list_.create_item("Test Content")
        assert_equal([b"<ul>", b'<li>', b"Test Content", b"</li>", b"</ul>"],
                     list(iter(list_)))

    def test_create_items(self):
        list_ = UnorderedList()
        items = list_.create_items("foo", "bar", "baz")
        assert_equal([b"<ul>",
                      b"<li>", b"foo", b"</li>",
                      b"<li>", b"bar", b"</li>",
                      b"<li>", b"baz", b"</li>",
                      b"</ul>"],
                     list(iter(list_)))
        assert_equal(3, len(items))


class ListItemTest(TestCase):

    def test_without_initial_content(self):
        li = ListItem()
        li.append("Test")
        assert_equal([b"<li>", b"Test", b"</li>"], list(iter(li)))

    def test_with_initial_content(self):
        li = ListItem("Initial", "test")
        li.append("content")
        assert_equal([b"<li>", b"Initial", b"test", b"content", b"</li>"],
                     list(iter(li)))


class DescriptionListTest(TestCase):

    def test_create_term(self):
        dl = DescriptionList()
        dl.create_item("Term", "Description")
        assert_equal([b"<dl>", b"<dt>", b"Term", b"</dt>", b"<dd>",
                      b"Description", b"</dd>", b"</dl>"], list(iter(dl)))
