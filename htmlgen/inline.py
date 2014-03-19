from htmlgen.element import Element


class Span(Element):

    """An HTML in-line <span> element.

    <span> elements are inline elements without semantic meaning. They are
    containers for styling or scripting.


        >>> span1 = Span("Example text")
        >>> span2 = Span()
        >>> span2.append("Example text")

    """

    def __init__(self, content=None):
        super(Span, self).__init__("span")
        if content:
            self.append(content)
