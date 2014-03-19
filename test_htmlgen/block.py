from unittest import TestCase

from asserts import assert_equal

from htmlgen import Division, Paragraph, Preformatted


class DivisionTest(TestCase):

    def test_render(self):
        div = Division()
        div.append("Test")
        assert_equal([b"<div>", b"Test", b"</div>"], list(iter(div)))


class ParagraphTest(TestCase):

    def test_without_initial_content(self):
        p = Paragraph()
        p.append("Test")
        assert_equal([b"<p>", b"Test", b"</p>"], list(iter(p)))

    def test_with_initial_content(self):
        p = Paragraph("Initial")
        p.append("Test")
        assert_equal([b"<p>", b"Initial", b"Test", b"</p>"], list(iter(p)))


class PreformattedTest(TestCase):

    def test_render(self):
        div = Preformatted()
        div.append("Test")
        assert_equal([b"<pre>", b"Test", b"</pre>"], list(iter(div)))
