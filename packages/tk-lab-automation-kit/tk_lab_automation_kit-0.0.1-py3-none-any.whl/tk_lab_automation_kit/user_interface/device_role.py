from tkinter import StringVar


class DeviceRole(object):
    """
    Represents a device role and a set of possible devices to be assigned to it.
    """

    @property
    def choice(self):
        """
        The currently selected choice of device to occupy this role.
        :return:
        """
        return self.selected.get()

    def __init__(self, parent, choices, choice=None):
        self._root = parent    # keep reference to the ui root
        # selection variable for option menu
        self.selected = StringVar(parent, list(choices)[0] if choice is None else choice)
        self.choices = choices  # set of choices in the option menu