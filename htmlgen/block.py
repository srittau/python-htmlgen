from htmlgen.element import Element


class Division(Element):

    """An HTML division (<div>) element.

    <div> elements are block-level elements without semantic meaning. They are
    containers for styling or scripting.

        >>> div = Division()
        >>> div.id = "my-block"
        >>> div.add_css_classes("important", "legal")
        >>> div.append("This is important legal text.")

    """

    def __init__(self):
        super(Division, self).__init__("div")


class Paragraph(Element):

    """An HTML paragraph (<p>) element.

    <p> elements are block-level elements that delineate text paragraphs.

        >>> p1 = Paragraph("This is a text paragraph.")
        >>> p2 = Paragraph()
        >>> p2.append("This is another paragraph.")

    """

    def __init__(self, content=None):
        super(Paragraph, self).__init__("p")
        if content:
            self.append(content)


class Preformatted(Element):

    """An HTML pre-formatted text (<pre>) element.

    <pre> elements are block-level elements that contain text which will
    be displayed as is. E.g. all white-space is kept and the text is
    usually played with a non-proportional font.

        >>> pre = Preformatted()
        >>> pre.append("Hello\\nWorld!")

    """

    def __init__(self):
        super(Preformatted, self).__init__("pre")
