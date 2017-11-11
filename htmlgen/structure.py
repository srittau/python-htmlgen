from htmlgen.element import Element


class Section(Element):

    """An HTML sectioning (<section>) element.

    Sections are logical units in a document, like chapter and sub-chapters.

    """

    def __init__(self):
        super(Section, self).__init__("section")


class Article(Element):

    """An HTML article (<article>) element.

    A self-contained article on a page, like a blog entry or a comment in a
    blog system.

    """

    def __init__(self):
        super(Article, self).__init__("article")


class Navigation(Element):

    """An HTML navigation container (<nav>) element."""

    def __init__(self):
        super(Navigation, self).__init__("nav")


class Aside(Element):

    """An HTML element for tangential related content (<aside>).
    """

    def __init__(self):
        super(Aside, self).__init__("aside")


class Header(Element):

    """An HTML header (<header>) element.

    Header elements group multiple headings and related contents
    of a section or page.

    """

    def __init__(self):
        super(Header, self).__init__("header")


class Footer(Element):

    """An HTML footer (<footer>) element.

    Footer elements group the footer elements of a section or page.

    """

    def __init__(self):
        super(Footer, self).__init__("footer")


class Heading(Element):

    """A page or section heading (<h1> to <h6>) HTML element.

    Headings have a level between 1 and 6, where a lower number
    means a more important heading. In general, the main heading
    of a page or section uses a level 1 heading, while sub-levels
    use a level 2 heading. Headings should be grouped with Header
    elements.

        >>> header = Header()
        >>> header.append(Heading(1, "Hello World!"))
        >>> header.append(Heading(2, "The philosophical ramification of "
        ...                          "programming in a postmodern society"))
        >>> str(header)
        '<header><h1>Hello World!</h1><h2>The philosophical ramification of programming in a postmodern society</h2></header>'

    """

    def __init__(self, level=1, *content):
        if level < 1 or level > 6:
            raise TypeError("heading level must be between 1 and 6")
        super(Heading, self).__init__("h" + str(level))
        self.level = level
        self.extend(content)
