import os
import json
from tkinter import Button, Label, Checkbutton, Entry
from tk_lab_automation_kit.user_interface import CustomFrame, ConfigParameter


class ParameterTable(CustomFrame):
    """
    A UI control that creates a table from a given set of parameters so they can easily be set from the UI.
    """
    @property
    def parameter_source(self):
        """
        Gets the currently set parameter dictionary.
        :return: dictionary with ConfigParameter objects as values
        """
        return self._parameter_source

    @parameter_source.setter
    def parameter_source(self, source):
        """
        Sets the parameter dictionary.
        :param source: dictionary with the parameter names as keys and ConfigParameter objects as values
        """
        self._parameter_source = source
        self._setup_()    # redraw the control with the new parameter source

    @property
    def show_apply_button(self):
        """
        Gets if apply button is shown
        :return: True or False
        """
        return self._show_apply_button

    @show_apply_button.setter
    def show_apply_button(self, v):
        """
        Sets if apply button is shown
        :param v: True or False
        """
        self._show_apply_button = v
        self._apply_button.grid_forget()
        if self._show_apply_button:
            self._apply_button.grid(row=self._row_count, column=0, sticky='w', padx=2, pady=2)

    @property
    def apply_command(self):
        return self._apply_command

    @apply_command.setter
    def apply_command(self, value):
        self._apply_command = value

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)   # call the parent class's constructor
        self._root = parent    # keep reference to the ui parent
        self._apply_command = None  # store command which gets executed when the apply button is clicked
        self._parameter_source = None
        self._show_apply_button = False
        self._row_count = 0
        self._setup_()        # draw the table
    
    def _setup_(self):
        self.clear()    # remove all existing ui controls from the table

        self._apply_button = Button(self, text='apply', command=self._run_apply_command_)
        self._children.append(self._apply_button)
        self.show_apply_button = self._show_apply_button

        if self.parameter_source is None:   # do nothing if no parameters are set
            return

        # add the fields for all the parameters
        r = 0
        for parameter_name in self.parameter_source:
            parameter = self.parameter_source[parameter_name]       # get the next parameter
            self.add_widget(Label(self, text='{}:'.format(parameter_name)), row=r, column=0, sticky='w')    # add parameter name

            if parameter.parameter_type == 'bool':
                self.add_widget(Checkbutton(self, variable=parameter.variable), row=r, column=1, sticky='w')
            else:
                self.add_widget(Entry(self, textvariable=parameter.variable), row=r, column=1, sticky='w')  # add entry to edit value

            if not parameter.unit is None:
                self.add_widget(Label(self, text='[{}]'.format(parameter.unit)), row=r, column=2, sticky='w')  # add unit description

            # add browse button for files and folders
            if parameter.parameter_type == 'folder':
                self.add_widget(
                    Button(self, text='browse...', command=parameter.browse_folders), 
                    row=r, column=2, padx=5)
            if parameter.parameter_type == 'file':
                self.add_widget(
                    Button(self, text='browse...', command=parameter.browse_files), 
                    row=r, column=2, padx=5)
            r += 1
        self._row_count = r

        self.show_apply_button = self._show_apply_button

    def _run_apply_command_(self):
        if self.apply_command is not None:
            self.apply_command()

    def serialize(self, path):
        """
        Serializes data in table to json.
        :param path: path to save the serialized data to
        """
        if self._parameter_source is None:
            return
        data = {}
        for parameter_name in self._parameter_source:
            if not type(self._parameter_source[parameter_name]) is ConfigParameter:
                raise TypeError('The given type is invalid, expected "{}" but got "{}".'.format(ConfigParameter, type(self._parameter_source[parameter_name])))

            data[parameter_name] = self._parameter_source[parameter_name].value
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    def deserialize(self, path):
        """
        Deserializes the table data from a given file and loads it into the cells.
        :param path: path where the file with the serialized data is located
        """
        if self._parameter_source is None or not os.path.isfile(path):
            return
        with open(path, 'r') as json_file:
            data = json.loads(json_file.read())
        for parameter_name in data:
            self._parameter_source[parameter_name].value = data[parameter_name]
        self._setup_()