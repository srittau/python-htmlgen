from .attribute import html_attribute
from .element import VoidElement


class Image(VoidElement):

    """An HTML image (<img>) element.

    Images must have an alternate text description that describes the
    contents of the image, if the image can not be displayed. In some
    cases the alternate text can be empty. For example, if the image just
    displays a company logo next to the company's name or if the image just
    adds an icon next to a textual description of an action.

    Example:

        >>> image = Image("whiteboard.jpg",
        ...               "A whiteboard filled with mathematical formulas.")
        >>> image.title = "Whiteboards are a useful tool"

    """

    def __init__(self, url, alternate_text=""):
        super(Image, self).__init__("img")
        self.url = url
        self.alternate_text = alternate_text

    url = html_attribute("src")
    alternate_text = html_attribute("alt")
    title = html_attribute("title")
