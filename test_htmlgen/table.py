from unittest import TestCase

from asserts import assert_equal, assert_true

from htmlgen import Table, TableHead, TableRow, TableCell, ColumnGroup, Span


class TableTest(TestCase):

    def test_empty(self):
        table = Table()
        assert_equal([b"<table>", b"</table>"], list(iter(table)))

    def test_create_head_and_body(self):
        table = Table()
        table.create_body()
        table.create_head()
        table.create_row()
        table.create_header_row()
        assert_equal([b"<table>",
                      b"<thead>", b"<tr>", b"</tr>", b"</thead>",
                      b"<tbody>", b"<tr>", b"</tr>", b"</tbody>",
                      b"<tbody>", b"</tbody>",
                      b"<thead>", b"</thead>",
                      b"</table>"], list(iter(table)))

    def test_append_header_row__implicit_head(self):
        table = Table()
        row = TableRow()
        table.append_header_row(row)
        assert_equal([b"<table>", b"<thead>", b"<tr>", b"</tr>", b"</thead>",
                      b"</table>"], list(iter(table)))

    def test_create_header_row__implicit_head(self):
        table = Table()
        table.create_header_row()
        assert_equal([b"<table>", b"<thead>", b"<tr>", b"</tr>", b"</thead>",
                      b"</table>"], list(iter(table)))

    def test_create_header_row__row_object(self):
        table = Table()
        row = table.create_header_row()
        row.id = "my-row"
        assert_equal([b'<tr id="my-row">', b"</tr>"], list(iter(row)))

    def test_append_row__implicit_body(self):
        table = Table()
        row = TableRow()
        table.append_row(row)
        assert_equal([b"<table>", b"<tbody>", b"<tr>", b"</tr>", b"</tbody>",
                      b"</table>"], list(iter(table)))

    def test_create_row__implicit_body(self):
        table = Table()
        table.create_row()
        assert_equal([b"<table>", b"<tbody>", b"<tr>", b"</tr>", b"</tbody>",
                      b"</table>"], list(iter(table)))

    def test_create_row__row_object(self):
        table = Table()
        row = table.create_row()
        row.id = "my-row"
        assert_equal([b'<tr id="my-row">', b"</tr>"], list(iter(row)))

    def test_children_order(self):
        table = Table()
        table.append_raw("<tr>Bare line</tr>")
        table.create_row()
        table.create_header_row()
        assert_equal([b"<table>",
                      b"<thead>", b"<tr>", b"</tr>", b"</thead>",
                      b"<tbody>", b"<tr>", b"</tr>", b"</tbody>",
                      b"<tr>Bare line</tr>",
                      b"</table>"], list(iter(table)))

    def test_create_simple_header_row(self):
        table = Table()
        table.create_simple_header_row("Col 1", "Col 2")
        assert_equal("<table><thead><tr><th>Col 1</th><th>Col 2</th></tr>"
                     "</thead></table>", str(table))

    def test_create_simple_header_row__returned_row(self):
        table = Table()
        row = table.create_simple_header_row()
        row.id = "test-id"
        assert_equal('<table><thead><tr id="test-id"></tr></thead></table>',
                     str(table))

    def test_create_simple_row(self):
        table = Table()
        table.create_simple_row("Col 1", "Col 2")
        assert_equal("<table><tbody><tr><td>Col 1</td><td>Col 2</td></tr>"
                     "</tbody></table>", str(table))

    def test_create_simple_row__returned_row(self):
        table = Table()
        row = table.create_simple_row()
        row.id = "test-id"
        assert_equal('<table><tbody><tr id="test-id"></tr></tbody></table>',
                     str(table))

    def test_generate_header_rows(self):
        class MyTable(Table):
            def generate_header_rows(self):
                yield TableRow()
        table = MyTable()
        assert_equal('<table><thead><tr></tr></thead></table>', str(table))

    def test_generate_rows(self):
        class MyTable(Table):
            def generate_rows(self):
                yield TableRow()
        table = MyTable()
        assert_equal('<table><tbody><tr></tr></tbody></table>', str(table))


class TableHeadTest(TestCase):

    def test_create_row(self):
        head = TableHead()
        row = head.create_row()
        row.id = "my-row"
        assert_equal('<thead><tr id="my-row"></tr></thead>', str(head))


class TableRowTest(TestCase):

    def test_create_cell(self):
        row = TableRow()
        cell1 = row.create_cell()
        cell1.append("Cell 1")
        row.create_cell("Cell 2")
        assert_equal("<tr><td>Cell 1</td><td>Cell 2</td></tr>", str(row))

    def test_create_cells(self):
        row = TableRow()
        row.create_cells("Cell 1", "Cell 2")
        assert_equal('<tr><td>Cell 1</td><td>Cell 2</td></tr>', str(row))

    def test_create_cells_return_value(self):
        row = TableRow()
        cells = row.create_cells("Cell 1", "Cell 2")
        assert_equal(2, len(cells))

    def test_create_header_cell(self):
        row = TableRow()
        cell1 = row.create_header_cell()
        cell1.append("Cell 1")
        row.create_header_cell("Cell 2")
        assert_equal("<tr><th>Cell 1</th><th>Cell 2</th></tr>", str(row))

    def test_create_header_cells(self):
        row = TableRow()
        row.create_header_cells("Cell 1", "Cell 2")
        assert_equal('<tr><th>Cell 1</th><th>Cell 2</th></tr>', str(row))

    def test_create_header_cells_return_value(self):
        row = TableRow()
        cells = row.create_header_cells("Cell 1", "Cell 2")
        assert_equal(2, len(cells))


class TableCellTest(TestCase):

    def test_default_columns_and_rows(self):
        cell = TableCell("Content")
        assert_equal(1, cell.columns)
        assert_equal(1, cell.rows)
        assert_equal('<td>Content</td>', str(cell))

    def test_columns_and_rows(self):
        cell = TableCell("Content")
        cell.columns = 3
        cell.rows = 5
        assert_equal('<td colspan="3" rowspan="5">Content</td>', str(cell))

    def test_element_child(self):
        cell = TableCell(Span("Content"))
        assert_equal('<td><span>Content</span></td>', str(cell))


class ColumnGroupTest(TestCase):

    def test_create_column(self):
        group = ColumnGroup()
        col = group.create_column()
        col.add_css_classes("col-cls")
        group.create_column()
        assert_equal('<colgroup><col class=\"col-cls\"></col><col></col>'
                     '</colgroup>', str(group))

    def test_create_columns_with_classes(self):
        group = ColumnGroup()
        cols = group.create_columns_with_classes("cls1", "cls2")
        assert_equal(2, len(cols))
        assert_true(cols[0].has_css_class("cls1"))
