from unittest import TestCase

from asserts import assert_equal

from htmlgen.link import Link


class LinkTest(TestCase):

    def test_simple(self):
        link = Link("foo")
        assert_equal([b'<a href="foo">', b"</a>"], list(iter(link)))

    def test_caption_argument(self):
        link = Link("foo", "initial", "caption")
        link.append(" continued")
        assert_equal([b'<a href="foo">', b"initial", b"caption", b" continued",
                      b"</a>"], list(iter(link)))

    def test_url(self):
        link = Link("initial-url")
        assert_equal("initial-url", link.url)
        link.url = "new-url"
        assert_equal([b'<a href="new-url">', b"</a>"], list(iter(link)))

    def test_target(self):
        link = Link("")
        assert_equal("_self", link.target)
        link.target = "my-target"
        assert_equal([b'<a href="" target="my-target">', b"</a>"],
                     list(iter(link)))
        link.set_blank_target()
        assert_equal("_blank", link.target)
        assert_equal([b'<a href="" target="_blank">', b"</a>"],
                     list(iter(link)))

    def test_title(self):
        link = Link("foo")
        link.title = "Test Title"
        assert_equal([b'<a href="foo" title="Test Title">', b"</a>"],
                     list(iter(link)))
