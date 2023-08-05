from tkinter import DoubleVar, IntVar, BooleanVar, IntVar, StringVar, NORMAL, DISABLED


class CustomTableCell(object):
    """
    The cell populates a custom table row. It has its own data type.
    """

    @property
    def value(self):
        """
        Gets value of the cell.
        :return: cell data
        """
        return self.variable.get()

    @value.setter
    def value(self, val):
        """
        Sets value of the cell.
        :param val: value to set the cell to
        """
        self.variable.set(val)

    @property
    def is_enabled(self):
        """
        Gets if the cell can be edited.
        :return: True or False
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, val):
        """
        Sets if the cell can be edited (cell will be grayed out if set to False)
        :param val: True or False
        """
        self._is_enabled = val

        if self.control_handle is not None:  # if a widget is using this cell set the appropriate state
            self.control_handle.config(state=NORMAL if self._is_enabled else DISABLED)

        for callback in self.enabled_changed:   # notify any subscribers about the change
            callback(self, self._is_enabled)

    def __init__(self, parent, cell_value=None, cell_type='float', name=None, unit=None, is_enabled=True):
        self._root = parent         # keep reference to the containing element
        self.cell_type = cell_type  # store the type of the cell (used for display of correct widget in the table)
        self.variable = None        # space for the tkinter variable
        self.enabled_changed = list()   # callback list to subscribe to the enabled changed event
        self.control_handle = None      # handle to the widget that uses this cell as data source
        self.name = name    # name of the cell (used to access it quickly via the CustomTableSource data structure)
        self.unit = unit    # the physical unit of this cell (if not None this will add the units in [] after the cell)
        self.is_enabled = is_enabled    # sets if the user can edit this cell

        # setup cell properties for various data types
        if cell_type == 'float' or cell_type == 'double':
            if cell_value is None: cell_value = 0
            self.variable = DoubleVar(parent, cell_value)
        elif cell_type == 'int':
            if cell_value is None: cell_value = 0
            self.variable = IntVar(parent, cell_value)
        elif cell_type == 'bool':
            if cell_value is None: cell_value = False
            self.variable = BooleanVar(parent, cell_value)
        elif cell_type == 'empty':
            self.variable = IntVar()
        else:
            self.variable = StringVar(parent, cell_value)