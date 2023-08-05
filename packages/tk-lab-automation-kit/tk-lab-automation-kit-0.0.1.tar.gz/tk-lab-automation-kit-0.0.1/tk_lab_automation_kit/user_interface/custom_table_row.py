from tk_lab_automation_kit.user_interface import CustomTableCell


class CustomTableRow(object):
    """
    A row that makes up a custom table source.
    """

    def __iter__(self):
        """Iterator used for loop statements over all cells in this row."""
        for cell in self._cells:
            yield cell

    def __getitem__(self, index):
        """Returns the cell at the specified index (column)."""
        return self._cells[index]

    def __setitem__(self, index, value: CustomTableCell):
        """Sets the cell at the specified index (column)."""
        self._cells[index] = value

    def append(self, value: CustomTableCell):
        """
        Append cell to row.
        :param value: CustomCell to append to the row
        """
        self._cells.append(value)

    @property
    def cells(self):
        """
        Gets the cells of this row.
        :return: collection of CustomCell objects
        """
        return self._cells

    @cells.setter
    def cells(self, value):
        """
        Sets the cells of this row.
        :param value: collection of CustomCell objects
        """
        self._cells = value

    def __init__(self, parent, *args):
        self._cells = list()    # initialize cells of this row
        self._root = parent     # store reference to containing object

        for cell in args:       # add cells
            self.append(cell)
