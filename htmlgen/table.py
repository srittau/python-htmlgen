from htmlgen.attribute import int_html_attribute
from htmlgen.element import Element


class Table(Element):

    """An HTML table (<table>) element.

        >>> table = Table()
        >>> row = table.create_row()
        >>> cell = row.create_cell("My Cell")
        >>> cell.id = "my-cell"
        >>> str(table)
        '<table><tbody><tr><td id="my-cell">My Cell</td></tr></tbody></table>'

    More control over the table head and body elements is possible, using
    either create_head() and create_body() or appending TableHead and TableBody
    elements.

        >>> table = Table()
        >>> body = table.create_body()
        >>> head = table.create_head()
        >>> table.append(TableBody())

    It is also possible to override the generate_header_rows() and
    generate_rows() methods:

        >>> class MyTable(Table):
        ...     def generate_rows(self):
        ...         yield TableRow()
        >>> str(MyTable())
        '<table><tbody><tr></tr></tbody></table>'

    For simple tables, create_simple_header_row() and create_simple_row()
    can be used:

        >>> table = Table()
        >>> head = table.create_simple_header_row("Column 1", "Column 2")
        >>> row = table.create_simple_row("Content 1", "Content 2")

    """

    def __init__(self):
        super(Table, self).__init__("table")
        self._head = TableHead()
        self._body = TableBody()

    def create_head(self):
        """Create a TableHead element, append and return it.

            >>> table = Table()
            >>> head = table.create_head()
            >>> head.id = "my-head"
            >>> str(table)
            '<table><thead id="my-head"></thead></table>'

        """
        header = TableHead()
        self.append(header)
        return header

    def create_header_row(self):
        """Create a TableRow, append it to the head section, and return it.

            >>> table = Table()
            >>> row = table.create_header_row()
            >>> row.id = "my-row"
            >>> str(table)
            '<table><thead><tr id="my-row"></tr></thead></table>'

        The row will be added using append_header_row(). See there for
        details.

        """
        return self._head.create_row()

    def create_body(self):
        """Create a TableBody element, append and return it.

            >>> table = Table()
            >>> body = table.create_body()
            >>> body.id = "my-body"
            >>> str(table)
            '<table><tbody id="my-body"></tbody></table>'

        """
        body = TableBody()
        self.append(body)
        return body

    def create_row(self):
        """Create a TableRow, append it to the body section, and return it.

            >>> table = Table()
            >>> row = table.create_row()
            >>> row.id = "my-row"
            >>> str(table)
            '<table><tbody><tr id="my-row"></tr></tbody></table>'

        The row will be added using append_row(). See there for details.

        """
        return self._body.create_row()

    def append_header_row(self, row):
        """Append a table row to the implicit table head section.

            >>> table = Table()
            >>> table.append_header_row(TableRow())

        All rows added this way will be added to an implicitly created
        TableHead section at the beginning of the table, before any other
        children.

            >>> table = Table()
            >>> table.append_raw("<tr>Manual row</tr>")
            >>> table.append_header_row(TableRow())
            >>> str(table)
            '<table><thead><tr></tr></thead><tr>Manual row</tr></table>'

        """
        self._head.append(row)

    def append_row(self, row):
        """Append a table row to the implicit table body section.

            >>> table = Table()
            >>> table.append_row(TableRow())

        All rows added this way will be added to an implicitly created
        TableBody section at the beginning of the table, after an implicit
        TableHead, and before any other children.

            >>> table = Table()
            >>> table.append_raw("<tr>Manual row</tr>")
            >>> table.append_row(TableRow())
            >>> table.append_header_row(TableRow())
            >>> str(table)
            '<table><thead><tr></tr></thead><tbody><tr></tr></tbody><tr>Manual row</tr></table>'

        """
        self._body.append(row)

    def create_simple_header_row(self, *headers):
        """Create a TableRow with text cells and append it to the table head.

            >>> table = Table()
            >>> row = table.create_simple_header_row("Column 1", "Column 2")
            >>> row.id = "my-id"
            >>> str(table)
            '<table><thead><tr id="my-id"><th>Column 1</th><th>Column 2</th></tr></thead></table>'

        """
        row = self.create_header_row()
        row.create_header_cells(*headers)
        return row

    def create_simple_row(self, *cells):
        """Create a TableRow with text cells and append it to the table.

            >>> table = Table()
            >>> row = table.create_simple_row("Column 1", "Column 2")
            >>> row.id = "my-id"
            >>> str(table)
            '<table><tbody><tr id="my-id"><td>Column 1</td><td>Column 2</td></tr></tbody></table>'

        """
        row = self.create_row()
        row.create_cells(*cells)
        return row

    def generate_children(self):
        if self._head.children:
            yield self._head
        head = TableHead()
        head.extend(self.generate_header_rows())
        if len(head):
            yield head
        if len(self._body):
            yield self._body
        body = TableBody()
        body.extend(self.generate_rows())
        if len(body):
            yield body
        for child in self.children:
            yield child

    def generate_header_rows(self):
        """Return an iterator over rows of this table's head.

        This method can be overridden by sub-classes.

        """
        if False:
            yield

    def generate_rows(self):
        """Return an iterator over rows of this table's body.

        This method can be overridden by sub-classes.

        """
        if False:
            yield


class _TableSection(Element):

    def create_row(self):
        """Create a TableRow, append it to this section, and return it."""
        row = TableRow()
        self.append(row)
        return row


class TableHead(_TableSection):

    """An HTML table head (<thead>) element.

        >>> head = TableHead()
        >>> row = head.create_row()
        >>> row.id = "my-row"
        >>> str(head)
        '<thead><tr id="my-row"></tr></thead>'

    """

    def __init__(self):
        super(TableHead, self).__init__("thead")


class TableBody(_TableSection):

    """An HTML table body (<tbody>) element.

        >>> body = TableBody()
        >>> row = body.create_row()
        >>> row.id = "my-row"
        >>> str(body)
        '<tbody><tr id="my-row"></tr></tbody>'

    """

    def __init__(self):
        super(TableBody, self).__init__("tbody")


class TableRow(Element):

    """An HTML table row (<tr>) element.

        >>> row = TableRow()
        >>> cell1 = row.create_cell("Cell 1")
        >>> cell2 = row.create_cell()
        >>> cell2.append("Cell 2")
        >>> str(row)
        '<tr><td>Cell 1</td><td>Cell 2</td></tr>'

    """

    def __init__(self):
        super(TableRow, self).__init__("tr")

    def create_cell(self, content=""):
        """Create a TableCell, append it to this row, and return it.

        An initial child can be supplied.

        """
        cell = TableCell(content)
        self.append(cell)
        return cell

    def create_cells(self, *content):
        """Create multiple TableCells and return them.

            >>> row = TableRow()
            >>> cells = row.create_cells("Cell 1", "Cell 2")
            >>> cells[0].id = "my-cell"
            >>> str(row)
            '<tr><td id="my-cell">Cell 1</td><td>Cell 2</td></tr>'

        """
        return [self.create_cell(cell) for cell in content]

    def create_header_cell(self, content=""):
        """Create a TableHeaderCell, append it to this row, and return it.

        An initial child can be supplied.

        """

        cell = TableHeaderCell(content)
        self.append(cell)
        return cell

    def create_header_cells(self, *content):
        """Create multiple TableHeaderCells and return them.

            >>> row = TableRow()
            >>> cells = row.create_header_cells("Cell 1", "Cell 2")
            >>> cells[0].id = "my-cell"
            >>> str(row)
            '<tr><th id="my-cell">Cell 1</th><th>Cell 2</th></tr>'

        """
        return [self.create_header_cell(cell) for cell in content]


class _TableCellBase(Element):

    def __init__(self, element_name, *content):
        super(_TableCellBase, self).__init__(element_name)
        self.extend(content)

    rows = int_html_attribute("rowspan", 1)
    columns = int_html_attribute("colspan", 1)


class TableHeaderCell(_TableCellBase):

    """An HTML table header cell (<th>) element.

        >>> cell1 = TableHeaderCell("Content")
        >>> cell1.columns = 3
        >>> cell1.rows = 2
        >>> cell2 = TableHeaderCell()
        >>> cell2.append("Content")

    """

    def __init__(self, *content):
        super(TableHeaderCell, self).__init__("th", *content)


class TableCell(_TableCellBase):

    """An HTML table cell (<td>) element.

        >>> cell1 = TableCell("Content")
        >>> cell1.columns = 3
        >>> cell1.rows = 2
        >>> cell2 = TableCell()
        >>> cell2.append("Content")

    """

    def __init__(self, *content):
        super(TableCell, self).__init__("td", *content)


class ColumnGroup(Element):

    """An HTML column group (<colgroup>) element.

        >>> group = ColumnGroup()
        >>> col = group.create_column()
        >>> col.add_css_classes("column-class")

    """

    def __init__(self):
        super(ColumnGroup, self).__init__("colgroup")

    def create_column(self):
        """Create a column, append it to this group, and return it."""
        column = Column()
        self.append(column)
        return column

    def create_columns_with_classes(self, *css_classes):
        """Create multiple columns with CSS classes."""
        def create_column(css):
            column = self.create_column()
            column.add_css_classes(css)
            return column
        return [create_column(css) for css in css_classes]


class Column(Element):

    """An HTML column (<col>) element."""

    def __init__(self):
        super(Column, self).__init__("col")
