from unittest import TestCase

from asserts import assert_equal

from htmlgen import (Span, Highlight, Strong, Alternate, Emphasis, Small,
                     LineBreak)


class SpanTest(TestCase):

    def test_without_initial_content(self):
        span = Span()
        span.append("Test")
        assert_equal([b"<span>", b"Test", b"</span>"], list(iter(span)))

    def test_with_initial_content(self):
        span = Span("Initial", "test")
        span.append("content")
        assert_equal([b"<span>", b"Initial", b"test", b"content", b"</span>"],
                     list(iter(span)))


class HighlightTest(TestCase):

    def test_without_initial_content(self):
        highlight = Highlight()
        highlight.append("Test")
        assert_equal([b"<b>", b"Test", b"</b>"], list(iter(highlight)))

    def test_with_initial_content(self):
        highlight = Highlight("Initial", "test")
        highlight.append("content")
        assert_equal([b"<b>", b"Initial", b"test", b"content", b"</b>"],
                     list(iter(highlight)))


class StrongTest(TestCase):

    def test_without_initial_content(self):
        strong = Strong()
        strong.append("Test")
        assert_equal([b"<strong>", b"Test", b"</strong>"], list(iter(strong)))

    def test_with_initial_content(self):
        strong = Strong("Initial", "test")
        strong.append("content")
        assert_equal([b"<strong>", b"Initial", b"test", b"content",
                      b"</strong>"], list(iter(strong)))


class AlternateTest(TestCase):

    def test_without_initial_content(self):
        alt = Alternate()
        alt.append("Test")
        assert_equal([b"<i>", b"Test", b"</i>"], list(iter(alt)))

    def test_with_initial_content(self):
        alt = Alternate("Initial", "test")
        alt.append("content")
        assert_equal([b"<i>", b"Initial", b"test", b"content", b"</i>"],
                     list(iter(alt)))


class EmphasisTest(TestCase):

    def test_without_initial_content(self):
        em = Emphasis()
        em.append("Test")
        assert_equal([b"<em>", b"Test", b"</em>"], list(iter(em)))

    def test_with_initial_content(self):
        em = Emphasis("Initial", "test")
        em.append("content")
        assert_equal([b"<em>", b"Initial", b"test", b"content", b"</em>"],
                     list(iter(em)))


class SmallTest(TestCase):

    def test_without_initial_content(self):
        small = Small()
        small.append("Test")
        assert_equal([b"<small>", b"Test", b"</small>"], list(iter(small)))

    def test_with_initial_content(self):
        small = Small("Initial", "test")
        small.append("content")
        assert_equal([b"<small>", b"Initial", b"test", b"content",
                      b"</small>"], list(iter(small)))


class LineBreakTest(TestCase):

    def test_line_break(self):
        br = LineBreak()
        assert_equal("<br/>", str(br))
