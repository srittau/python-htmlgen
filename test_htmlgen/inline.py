from unittest import TestCase

from asserts import assert_equal

from htmlgen import Span


class SpanTest(TestCase):

    def test_without_initial_content(self):
        span = Span()
        span.append("Test")
        assert_equal([b"<span>", b"Test", b"</span>"], list(iter(span)))

    def test_with_initial_content(self):
        span = Span("Initial")
        span.append("Test")
        assert_equal([b"<span>", b"Initial", b"Test", b"</span>"],
                     list(iter(span)))
