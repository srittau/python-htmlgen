from unittest import TestCase

from asserts import assert_equal

from htmlgen import Division


class DivisionTest(TestCase):

    def test_render(self):
        div = Division()
        div.append("Test")
        assert_equal([b"<div>", b"Test", b"</div>"], list(iter(div)))
