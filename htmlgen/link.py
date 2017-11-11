from htmlgen.attribute import html_attribute
from htmlgen.element import Element


class Link(Element):

    """An HTML inline link (<a>) element.

        >>> link = Link("http://www.example.com/", "caption")
        >>> link.append(", more")
        >>> link.url
        'http://www.example.com/'
        >>> str(link)
        '<a href="http://www.example.com/">caption, more</a>'

    By default links open in the same window. This can be influenced using
    the target property:

        >>> link = Link("/foo/bar")
        >>> link.target
        '_self'
        >>> link.set_blank_target()
        >>> link.target
        '_blank'
        >>> link.target = "my-window"
        >>> str(link)
        '<a href="/foo/bar" target="my-window"></a>'

    Please refer to the HeadLink class for <link> elements.

    """

    def __init__(self, url, *content):
        super(Link, self).__init__("a")
        self.url = url
        self.extend(content)

    url = html_attribute("href")
    target = html_attribute("target", "_self")
    title = html_attribute("title")

    def set_blank_target(self):
        self.target = "_blank"
