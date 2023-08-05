import os
import json
from tkinter import OptionMenu, Label, font
from tk_lab_automation_kit.user_interface import CustomFrame


class DeviceSelector(CustomFrame):
    """
    A control that lists a set of device roles that can be assigned to a list of devices.
    """

    @property
    def device_source(self):
        """
        Gets the source dictionary of device roles.
        :return: Source dictionary with device roles
        """
        return self._device_source

    @device_source.setter
    def device_source(self, source):
        """
        Sets the source dictionary of device roles
        :param source: A dictionary with the role names as keys and DeviceRole as values
        """
        self._device_source = source
        self._setup_()    # redraw the control with the new data

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)   # call the parent class constructor
        self._root = parent    # save reference to ui root
        self._device_source = None
        self._setup_()        # draw the control

    def _set_width_(self, stringList, element):
        """Sets the width of the option menus according to the longest string"""
        f = font.nametofont(element.cget("font"))   # get font of ui element
        zerowidth = f.measure("0")  # get string width
        w = int(max([f.measure(i) for i in stringList]) / zerowidth)    # calculate max width
        element.config(width=w) # set width of control

    def _setup_(self):
        self.clear()    # remove all currently rendered controls inside the device selector

        if self.device_source is None:  # do nothing if no device roles are present
            return
         
        # create all ui elements
        r = 0
        for device in self._device_source:
            param = self._device_source[device]    # get device role
            self.add_widget(Label(self, text='{}:'.format(device)), row=r, column=0)    # add label with role name
            # add drop down option menu to choose devices
            menu = self.add_widget(OptionMenu(self, param.selected, *param.choices), row=r, column=1)
            self._set_width_(param.choices, menu)     # set width to longest device name
            r += 1

    def serialize(self, path):
        """
        Serializes data in table to json.
        :param path: path to save the serialized data to
        """
        if self._device_source is None:
            return
        data = {}
        for role_name in self._device_source:
            data[role_name] = self._device_source[role_name].choice
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    def deserialize(self, path):
        """
        Deserializes the table data from a given file and loads it into the cells.
        :param path: path where the file with the serialized data is located
        """
        if self._device_source is None or not os.path.isfile(path):
            return
        with open(path, 'r') as json_file:
            data = json.loads(json_file.read())
        for role_name in data:
            self._device_source[role_name].selected.set(data[role_name])
        self._setup_()