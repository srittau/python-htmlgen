from htmlgen.element import Element


class Division(Element):

    """A html division (<div>) element.

    <div> elements are block-level elements without semantic meaning. They are
    containers for styling or scripting.

        >>> div = Division()
        >>> div.id = "my-block"
        >>> div.add_css_classes("important", "legal")
        >>> div.append("This is important legal text.")

    """

    def __init__(self):
        super(Division, self).__init__("div")
