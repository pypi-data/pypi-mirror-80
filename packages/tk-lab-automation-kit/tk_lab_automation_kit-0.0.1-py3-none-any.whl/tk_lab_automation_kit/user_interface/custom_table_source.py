from tk_lab_automation_kit.core.observable_list import ObservableList


class CustomTableSource(ObservableList):
    """
    Data source for CustomTable, containing rows. It has a special accessor such that custom_table_source[name] will
    look up the name of the cell in all rows of the table source and return it.
    This prohibits the need to search through each row manually.
    """

    def __getitem__(self, key):
        """Accessor either returns a specific row or a cell if a name was given as index."""
        if type(key) is str:    # search the rows for the cell with the given name
            for row in self:
                for cell in row:
                    if cell.name == key:
                        return cell
        else:
            return super().__getitem__(key)  # return row at given index