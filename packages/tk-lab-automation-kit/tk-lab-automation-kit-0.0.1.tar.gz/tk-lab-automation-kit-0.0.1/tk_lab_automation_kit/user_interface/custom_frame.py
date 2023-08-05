from tkinter import LabelFrame, NORMAL, DISABLED, BooleanVar, Frame


class CustomFrame(LabelFrame):
    """
    Extended version of the tkinter frame. Provides some useful, general functionality.
    """

    @property
    def title(self):
        """
        Gets the title of the frame
        :return: title
        """
        return self._title

    @title.setter
    def title(self, txt):
        """
        Sets the title of the frame
        :param txt: title
        """
        if not type(txt) is str:
            raise TypeError('Arguemt type error, expected "{}" but got "{}".'.format(str, type(txt)))

        self.config(text=txt)
        self._title = txt

    @property
    def enabled(self):
        """
        Gets if this control is enabled.
        :return: True or False
        """
        return self._enabled_var.get() if self._enabled_var is not None else False

    @enabled.setter
    def enabled(self, value):
        """
        Sets if this control is enabled.
        :param value: True or False
        """
        if type(value) is BooleanVar:
            self._enabled_var = value
            self._enabled_var.trace_add("write", self._set_enabled_)
        elif type(value) is bool:
            self._enabled_var.set(value)
        else:
            raise ValueError('Unecpected type "{}" but "{}" was expected.'.format(type(value), bool))

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = list()
        self._title = ''
        self._enabled_var = BooleanVar(parent, True)

    def _set_enabled_(self, *args):
        is_enabled = self.enabled
        for child in self._children:
            if child is None or 'state' not in child.config():
                continue
            child.config(state=NORMAL if is_enabled else DISABLED)
            
    def clear(self):
        """
        Remove all child ui controls from the frame.
        """
        for child in self._children:
            child.grid_forget()
        self._children = []

    def add_widget(self, widget, **kwargs):
        """
        Add child ui control to the frame and place it in the grid structure of the frame.
        :param widget: widget to add
        :param kwargs: arguments for positioning the widget inside the grid
        :return: widget that was added
        """
        widget.grid(**kwargs)
        self._children.append(widget)
        return widget
