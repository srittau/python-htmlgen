from htmlgen.attribute import int_html_attribute
from htmlgen.element import Element


class _ListBase(Element):

    """Base class for HTML list elements."""

    def create_item(self, child=None):
        """Create a ListItem element and add it to this list."""
        item = ListItem()
        if child:
            item.append(child)
        self.append(item)
        return item

    def create_items(self, *items):
        """Create ListItem elements and add them to this list."""
        list_items = []
        for item in items:
            list_items.append(self.create_item(item))
        return list_items


class OrderedList(_ListBase):

    """An HTML ordered list (<ol>) element.

    It contains ListItem children.

        >>> list_ = OrderedList()
        >>> item = list_.create_item("First Item")
        >>> item.add_css_classes("first-item")
        >>> list_.append(ListItem("Second Item"))

    """

    def __init__(self):
        super(OrderedList, self).__init__("ol")

    start = int_html_attribute("start", 1)


class UnorderedList(_ListBase):

    """An HTML unordered list (<ul>) element.

    It contains ListItem children.

        >>> list_ = UnorderedList()
        >>> item = list_.create_item("First Item")
        >>> item.add_css_classes("first-item")
        >>> list_.append(ListItem("Second Item"))

    """

    def __init__(self):
        super(UnorderedList, self).__init__("ul")


class ListItem(Element):

    """An HTML list item (<li>) element.

    These elements are used as children of OrderedList and UnorderedList.

    """

    def __init__(self, *content):
        super(ListItem, self).__init__("li")
        self.extend(content)


class DescriptionList(Element):

    """An HTML description list (<dl>) element.

    This used to be known as a "definition list" and is a list of terms and
    their descriptions.

        >>> dl = DescriptionList()
        >>> term, definition = dl.create_item("Term", "Long description.")
        >>> term.add_css_classes("my-term")
        >>> str(dl)
        '<dl><dt class="my-term">Term</dt><dd>Long description.</dd></dl>'

    """

    def __init__(self):
        super(DescriptionList, self).__init__("dl")

    def create_item(self, term, description):
        """Create term and definition elements and add them to the list.

        Returns a (term element, description element) tuple.

        """
        dt = DescriptionTerm(term)
        dd = DescriptionDefinition(description)
        self.append(dt)
        self.append(dd)
        return dt, dd


class DescriptionTerm(Element):

    """An HTML term element (<dt>) for description lists."""

    def __init__(self, *content):
        super(DescriptionTerm, self).__init__("dt")
        self.extend(content)


class DescriptionDefinition(Element):

    """An HTML definition element (<dd>) for description lists."""

    def __init__(self, *content):
        super(DescriptionDefinition, self).__init__("dd")
        self.extend(content)
