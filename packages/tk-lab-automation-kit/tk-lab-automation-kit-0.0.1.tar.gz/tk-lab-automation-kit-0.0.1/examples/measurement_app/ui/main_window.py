import sys
from tkinter import Tk, Frame, Grid, Button
from tk_lab_automation_kit.user_interface import DeviceSelector, ParameterTable, ControlPanel, CustomTable, PlotControl
from examples.measurement_app.experiments import CustomAnalysisResultProvider
from examples.measurement_app.ui import MainWindowViewModel


class MainWindow(Frame):
    """
    This is the main window of the application.
    """

    def __init__(self, parent: Tk, view_model: MainWindowViewModel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)   # call parent constructor
        Grid.rowconfigure(parent, 0, weight=1)
        Grid.columnconfigure(parent, 0, weight=1)
        self._root = parent        # save reference to ui hierarchy root
        self._context = view_model # set data context of the main window
        self._table_settings_path = './table_settings.json'
        self._analyzer_settings_path = './analyzer_settings.json'
        self._source_settings_path = './source_settings.json'
        self._sidetone_settings_path = './sidetone_settings.json'
        self._plot_options_settings_path = './plot_options_settings.json'
        self._root.title(self._context.application_title) # window title
        self._root.geometry('{}x{}'.format(self._context.app_width, self._context.app_height))   # window size

        # connect to event in case the application closes and an experiment is still running.
        parent.protocol("WM_DELETE_WINDOW", self._on_close_)

        self.grid(row=0, column=0)  # place window in root element
        self._setup_()            # setup the main window content

    def _on_close_(self):
        self._analyzer_selector.serialize(self._analyzer_settings_path)
        self._signal_selector.serialize(self._source_settings_path)
        self._plot_options.serialize(self._plot_options_settings_path)
        self._side_tone_table.serialize(self._sidetone_settings_path)
        self._context.on_shutdown()
        self._root.destroy()
        sys.exit(0) # make sure application terminates (otherwise may get stuck because of running threads)

    def export_parameters(self):
        self._parameter_table.serialize(self._table_settings_path)

    def _setup_(self):
        """Setup main window"""

        # add device selector section for signal sources
        self._signal_selector = DeviceSelector(self._root)
        self._signal_selector.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self._signal_selector.title = 'Signal Generators'
        self._signal_selector.device_source = self._context.signal_generator_devices  # collection of devices
        self._signal_selector.deserialize(self._source_settings_path)

        # add device selector section for signal analyzer
        self._analyzer_selector = DeviceSelector(self._root)
        self._analyzer_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self._analyzer_selector.title = 'Signal Analyzer'
        self._analyzer_selector.device_source = self._context.signal_analyzer_devices  # collection of devices
        self._analyzer_selector.deserialize(self._analyzer_settings_path)

        # add parameter table which enables the configuration of the experiment
        self._parameter_table = ParameterTable(self._root)
        self._parameter_table.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        self._parameter_table.title = 'Experiment Parameters'
        self._parameter_table.enabled = self._context.enable_config
        self._parameter_table.parameter_source = self._context.parameters # parameter list
        self._parameter_table.deserialize(self._table_settings_path)
        self._default_button = Button(self._parameter_table, text='make default', command=self.export_parameters)
        self._default_button.grid(row=len(self._context.parameters), sticky='w', padx=2, pady=2)

        # add control panel which allows the starting and stopping of the experiment
        self._control_panel = ControlPanel(self._root)
        self._control_panel.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self._control_panel.title = 'Control'
        self._control_panel.button_width = 10
        self._control_panel.command_source = self._context.commands   # command list

        # add frequency control table
        self._main_tone_table = CustomTable(self._root)
        self._main_tone_table.title = 'Main Tones'
        self._main_tone_table.rows = self._context.main_tone_source
        self._main_tone_table.set_col_width(1, 13)
        self._main_tone_table.set_col_width(2, 13)
        self._main_tone_table.enabled = self._context.enable_config
        self._main_tone_table.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        self._side_tone_table = CustomTable(self._root)
        self._side_tone_table.title = 'Side Tones'
        self._side_tone_table.rows = self._context.side_tone_source
        self._side_tone_table.set_col_width(2, 13)
        self._side_tone_table.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
        self._side_tone_table.deserialize(self._sidetone_settings_path)

        # add plot region
        self._plot = PlotControl(self._root, add_toolbar=True, figsize=(5, 5))
        self._plot.title = 'Input-Output Power'
        self._plot.show_grid = True
        self._plot.data_source = self._context.plot_data
        self._plot.grid(row=1, column=2, columnspan=2, rowspan=2, padx=10, sticky='nsew')

        # add results table
        self._results = CustomTable(self._root)
        self._results.title = 'Results'
        self._results.rows = self._context.result_source
        self._results.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # add plot editor
        self._plot_options = ParameterTable(self._root)
        self._plot_options.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        self._plot_options.title = 'Plotting Options'
        self._plot_options.parameter_source = self._context.plot_option_parameters
        self._plot_options.enabled = self._context.enable_config
        self._plot_options.show_apply_button = True
        self._plot_options.apply_command = self._context.apply_plot_changes
        self._plot_options.deserialize(self._plot_options_settings_path)

        # resize with window
        for x in range(3):
            Grid.rowconfigure(self, x, weight=1)

        for x in range(3):
            Grid.columnconfigure(self, x, weight=1)


if __name__ == '__main__':
    from tkinter import Tk
    from examples.measurement_app.ui import MainWindowViewModel


    root = Tk()     # create root of user interface hierarchy
    view_model = MainWindowViewModel(root)      # create the view model for the main window (handles displayed data)
    main_window = MainWindow(root, view_model)  # create main window
    main_window.mainloop()  # display main window
