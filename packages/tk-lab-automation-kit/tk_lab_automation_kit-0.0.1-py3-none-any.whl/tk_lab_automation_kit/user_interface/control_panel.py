from tkinter import LabelFrame, NORMAL, DISABLED, BooleanVar, Frame, Button
from tk_lab_automation_kit.user_interface import CustomFrame, ControlCommand


class ControlPanel(CustomFrame):
    """
    This frame will be populated by buttons if a list of ControlCommands is set as its command_source.
    """

    @property
    def command_source(self):
        """
        Gets the command source of this control panel.
        :return: list of type ControlCommand
        """
        return self._command_source

    @command_source.setter
    def command_source(self, source):
        """
        Sets the command source. (Will produce buttons for each command in the source)
        :param source: list of type ControlCommand
        """
        self._command_source = source
        self._setup_()

    @property
    def button_width(self):
        """
        Gets the fixed with of all the buttons in the control panel.
        :return: width of buttons
        """
        return self._button_width

    @button_width.setter
    def button_width(self, width):
        """
        Sets the width of all the buttons on the control panel.
        :param width: width of the buttons
        """
        self._button_width = width
        self._setup_()

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._command_source = None
        self._button_width = None
        self._setup_()

    def _setup_(self):
        self.clear()

        if self._command_source is None:
            return

        r = 0
        for command in self._command_source:
            if not type(command) is ControlCommand:
                raise TypeError('Expected type "{}" but got "{}".'.format(ControlCommand, type(command)))

            command.button_handle = self.add_widget(
                Button(self, text=command.name, command=command.command), 
                row=r, padx=10, pady=5)
            if not self._button_width is None:
                command.button_handle.config(width=self._button_width)
            r += 1