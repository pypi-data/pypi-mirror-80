from tkinter import NORMAL, DISABLED


class ControlCommand(object):
    """
    This object is used as an item in the the control panel. It contains the command can can be enabled or disabled.
    """
    

    @property
    def can_execute(self):
        """
        Gets if this command can be executed (if false the associated button will be grayed out)
        :return: true or false
        """
        return self._can_execute

    @can_execute.setter
    def can_execute(self, b):
        """
        Sets if this command can be executed (will gray out associated button if set to False)
        :param b: True or False
        """
        self._can_execute = b
        self._update_can_execute_()

    @property
    def button_handle(self):
        """
        Gets the associated button object
        :return: widget
        """
        return self._button_handle

    @button_handle.setter
    def button_handle(self, handle):
        """
        Sets the associated button object
        :param handle: widget
        """
        self._button_handle = handle
        self._update_can_execute_()

    @property
    def name(self):
        return self._name

    @property
    def command(self):
        return self._command

    def __init__(self, command, name='', can_execute=True):
        self._name = name
        self._command = command
        self._can_execute = can_execute
        self._button_handle = None

    def _update_can_execute_(self):
        if not self.button_handle is None:
            self.button_handle.config(state=NORMAL if self._can_execute else DISABLED)