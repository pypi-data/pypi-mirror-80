import os
import json
from tkinter import Entry, Frame, Label, Checkbutton, NORMAL, DISABLED
from tk_lab_automation_kit.user_interface import CustomFrame, CustomTableSource


class CustomTable(CustomFrame):

    @property
    def rows(self):
        """
        Gets the rows of the table.
        :return: collection of rows of the table
        """
        return self._rows

    @rows.setter
    def rows(self, value):
        """
        Sets the rows of the table. This should be of the type CustomTableSource
        :param value: CustomTableSource
        """
        if self._rows is not None and type(self._rows) is CustomTableSource:
            self._rows.item_added.remove(self._row_added_)        # stop listening to changes of old source
            self._rows.item_removed.remove(self._row_removed_)    # stop listening to changes of old source

        self._rows = value  # set new row source

        if type(self._rows) is CustomTableSource:
            if self._row_added_ in self._rows.item_added:
                self._rows.item_added.remove(self._row_added_)        # start listening to changes of new source
            if self._row_added_ in self._rows.item_removed:
                self._rows.item_removed.remove(self._row_removed_)    # start listening to changes of new source

            self._column_widths = list()        # initialize column width list
            if len(self._rows) > 0:
                self._column_widths = [None for i in range(len(self._rows))]

        self._setup_()    # run setup to initialize all widgets that belong to the row data

    def get_col_width(self, col):
        """Gets the configured column width of the specified column."""
        return self._column_widths[col]

    def set_col_width(self, col, width):
        """
        Gets the configured column width of the specified column.
        :param col: Column index
        :param width: width of the column
        """
        self._column_widths[col] = width
        self._setup_()    # re-run setup to account for the change

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._rows = None
        self._column_widths = list()

    def _row_added_(self, row):
        self._setup_()    # re-run setup to account for the change

    def _row_removed_(self, row):
        self._setup_()    # re-run setup to account for the change

    def _setup_(self):
        self.clear()    # remove all existing widgets to clear the table

        if self._rows is None:  # do nothing if no row source is present
            return

        r = 0
        for row in self._rows:  # loop through all rows in the source
            c = 0
            for cell in row:    # loop through all cells in the current row source
                if c >= len(self._column_widths):
                    self._column_widths.append(None)    # add slot to column width list if it does not exist

                parent = self   # set parent to self if the widget has no unit label
                if cell.unit is not None:
                    '''if the cell has a unit label create a container frame where the unit label and the widget 
                    itself are positioned inside'''
                    cell_frame = self.add_widget(Frame(self), row=r, column=c)
                    parent = cell_frame

                # create widget according to cell type
                widget = None
                if cell.cell_type in ['float', 'int', 'double', 'text']:
                    widget = Entry(parent, textvariable=cell.variable, width=self._column_widths[c])
                elif cell.cell_type == 'label':
                    widget = Label(parent, textvariable=cell.variable, width=self._column_widths[c])
                elif cell.cell_type == 'bool':
                    widget = Checkbutton(parent, variable=cell.variable, width=self._column_widths[c])
                elif cell.cell_type == 'empty':
                    widget = Label(parent, width=self._column_widths[c])
                cell.control_handle = widget

                widget.config(state=NORMAL if cell.is_enabled else DISABLED)    # set widget enabled or disabled

                # add widget to table
                if cell.unit is not None:
                    self._children.append(widget)
                    widget.grid(row=0, column=0)
                    Label(parent, text='[{}]'.format(cell.unit)).grid(row=0, column=1)
                else:
                    self.add_widget(widget, row=r, column=c)
                c += 1
            r += 1

    def serialize(self, path):
        """
        Serializes data in table to json.
        :param path: path to save the serialized data to
        """
        if self.rows is None:
            return

        data = list()
        for row in self.rows:
            row_data = list()
            for cell in row:
                cell_data = dict()
                cell_data['cell_type'] = cell.cell_type
                cell_data['name'] = cell.name
                cell_data['unit'] = cell.unit
                cell_data['is_enabled'] = cell.is_enabled
                cell_data['value'] = cell.value
                row_data.append(cell_data)
            data.append(row_data)

        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    def deserialize(self, path):
        """
        Deserializes the table data from a given file and loads it into the cells.
        :param path: path where the file with the serialized data is located
        """
        if self.rows is None or not os.path.isfile(path):
            return
        with open(path, 'r') as json_file:
            data = json.loads(json_file.read())
            for row in range(len(data)):
                for col in range(len(data[row])):
                    cell = self.rows[row][col]
                    cell.value = data[row][col]['value']

