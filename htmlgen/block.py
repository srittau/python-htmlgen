from htmlgen.element import Element


class Division(Element):

    """A <div> element.

    <div> elements are block-level elements without semantic meaning. They are
    containers for styling or scripting.

    """
    def __init__(self):
        super(Division, self).__init__("div")
