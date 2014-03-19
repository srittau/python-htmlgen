from htmlgen import Element, int_html_attribute


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

    def __init__(self, content=None):
        super(ListItem, self).__init__("li")
        if content:
            self.append(content)
