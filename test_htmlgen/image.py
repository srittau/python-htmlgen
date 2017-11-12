from unittest import TestCase

from asserts import assert_equal

from htmlgen import Image

from test_htmlgen.util import parse_short_tag


class ImageTest(TestCase):

    def test_attributes(self):
        image = Image("my-image.png", "Alternate text")
        assert_equal("my-image.png", image.url)
        assert_equal("Alternate text", image.alternate_text)

    def test_attributes_default_alt(self):
        image = Image("my-image.png")
        assert_equal("", image.alternate_text)

    def test_with_alt(self):
        image = Image("my-image.png", "Alternate text")
        tag = parse_short_tag(str(image))
        assert_equal("img", tag.name)
        assert_equal("my-image.png", image.get_attribute("src"))
        assert_equal("Alternate text", image.get_attribute("alt"))

    def test_without_alt(self):
        image = Image("my-image.png")
        tag = parse_short_tag(str(image))
        assert_equal("img", tag.name)
        assert_equal("my-image.png", image.get_attribute("src"))
        assert_equal("", image.get_attribute("alt"))
