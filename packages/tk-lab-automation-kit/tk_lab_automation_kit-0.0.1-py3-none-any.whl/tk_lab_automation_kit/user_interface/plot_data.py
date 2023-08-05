from tk_lab_automation_kit.core import ObservableList


class PlotData(object):
    """
    This holds the data for a plot. It contains the x and y values as well as the type of plot.
    Keeps track of changes: If x or y change it will alert the plot to update.
    """

    @property
    def x(self):
        """
        Gets the x values of the plot.
        :return: x values
        """
        return self._x

    @x.setter
    def x(self, value):
        """
        Sets the x values of the plot and updates them.
        :param value: x values (ideally given as ObservableList, this enables the plot control to update this plot
        automatically)
        """
        if type(self._x) is ObservableList:     # if the old value was observable stop listening for changes
            self._x.item_added.append(self._item_changed_)
            self._x.item_removed.append(self._item_changed_)
        if type(value) is ObservableList:   # if the value it observable start listening for changes
            value.item_added.append(self._item_changed_)
            value.item_removed.append(self._item_changed_)
        self._x = value
        self._update_()

    @property
    def y(self):
        """
        Gets the y values of the plot.
        :return: y values
        """
        return self._y

    @y.setter
    def y(self, value):
        """
        Sets the y values of the plot and updates them.
        :param value: y values (ideally given as ObservableList, this enables the plot control to update this plot
        automatically)
        """
        if type(self._y) is ObservableList:      # if the old value was observable stop listening for changes
            self._y.item_added.append(self._item_changed_)
            self._y.item_removed.append(self._item_changed_)
        if type(value) is ObservableList:       # if the value is observable start listening for changes
            value.item_added.append(self._item_changed_)
            value.item_removed.append(self._item_changed_)
        self._y = value
        self._update_()

    _text = None

    @property
    def text(self):
        """
        Gets the text of this plot.
        :return: plot text
        """
        return self._text

    @text.setter
    def text(self, txt):
        """
        Sets the text of this plot.
        :param txt: plot text
        """
        if txt is not None and not type(txt) is str:
            raise TypeError('Given argument is of type "{}" but "{}" was expected.'.format(type(txt), str))

        self._text = txt
        self._update_()

    def __init__(self, x=None, y=None, text=None, plot_type='plot', **plot_args):
        self.data_changed = list()
        self._x = 0
        self._y = 0
        self.x = x
        self.y = y
        self.text = text
        self.plot_type = plot_type
        self.line_handle = None
        self.plot_args = plot_args
        self.plot_control = None

    def _item_changed_(self, item):
        """Gets called in case that x and y are observable and one of them has changed"""
        self._update_()

    def _update_(self):
        for callback in self.data_changed:
            callback(self)
