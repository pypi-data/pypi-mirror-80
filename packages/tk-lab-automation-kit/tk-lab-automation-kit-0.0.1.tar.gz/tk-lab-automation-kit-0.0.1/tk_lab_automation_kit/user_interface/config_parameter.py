from tkinter import DoubleVar, BooleanVar, StringVar, filedialog


class ConfigParameter(object):
    """
    Handles parameters for parameter tables.
    As a basis the tkinter.Variables are used which notify the ui about changes automatically.
    """

    @property
    def value(self):
        """
        Gets the current value of the parameter.
        :return: value of the parameter
        """
        return self.variable.get()

    @value.setter
    def value(self, v):
        """
        Sets the current value of the parameter.
        :param v: value
        """
        self.variable.set(v)

    def __init__(self, parent, value=0, unit=None, parameter_type='number'):
        # initialize the parameter either as a number or as text
        if parameter_type == 'number':
            self.variable = DoubleVar(parent, value)
        elif parameter_type == 'bool':
            self.variable = BooleanVar(parent, value)
        else:
            self.variable = StringVar(parent, value)
        self.unit = unit
        self.parameter_type = parameter_type

    def browse_folders(self):
        """
        Open folder browser.
        """
        result = filedialog.askdirectory(initialdir=self.value)
        if result is not None and result != '':
            self.value = result

    def browse_files(self):
        """
        Open file browser.
        """
        result = filedialog.asksaveasfilename(initialdir=self.value)
        if result is not None and result != '':
            self.value = result