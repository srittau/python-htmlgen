from htmlgen.element import Element


class Span(Element):

    """A <span> element.

    <span> elements are inline elements without semantic meaning. They are
    containers for styling or scripting.

    """

    def __init__(self):
        super(Span, self).__init__("span")
