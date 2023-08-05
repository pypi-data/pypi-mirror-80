import os
from tkinter import BooleanVar, filedialog
from pyscreenshot import grab
from datetime import datetime
from serial.tools import list_ports
from tk_lab_automation_kit.user_interface import CustomTableSource, CustomTableRow, CustomTableCell, ControlCommand, DeviceRole, ConfigParameter
from tk_lab_automation_kit.experiments import ExperimentHandler, message
from examples.measurement_app.experiments import CustomAnalysisResultProvider, CustomAnalysisPlotOptions, DemoExperiment


class MainWindowViewModel(object):
    """
    The view model for the main window. This class provides the data from the business logic to the view.
    """

    application_title = 'Two-Tone Experiment Tool'
    app_width = 1250
    app_height = 850

    def __init__(self, parent):
        self._root = parent    # save reference to ui root
        self.enable_config = BooleanVar(parent, True)

        # definitions for device selection
        self._get_signal_source_devices()  # get a set of devices that might be used as signal sources

        self.signal_generator_devices = dict()  # create empty dictionary to store device selection field data
        self.signal_generator_devices['Signal Source 1'] = DeviceRole(parent, self.signal_generator_set,
                                                            choice='TCPIP0::ief-lab-exg40g-1.ee.ethz.ch::inst0::INSTR')
        self.signal_generator_devices['Signal Source 2'] = DeviceRole(parent, self.signal_generator_set,
                                                            choice='COM11')
        # create dictionary which holds analyzer selection field data
        self.signal_analyzer_devices = {'Analyzer': DeviceRole(parent, {'TCPIP0::ief-lab-pxa-1.ee.ethz.ch::inst0::INSTR',})}

        # definitions for experiment parameters
        self.parameters = dict()
        self.parameters['device name'] = ConfigParameter(parent, value='RFAMP', parameter_type='text')
        self.parameters['filename suffix'] = ConfigParameter(parent, value='my_Experiment', parameter_type='text')
        self.parameters['out path'] = ConfigParameter(parent, value='./Experiments/TwoToneExperiment/Results/',
                                                      parameter_type='folder')
        self.parameters['measurement iterations'] = ConfigParameter(parent, value=1)     # measurement count to average
        self.parameters['resolution bandwidth'] = ConfigParameter(parent, value=2e3, unit='Hz')
        self.parameters['analyzer span'] = ConfigParameter(parent, value=4e6, unit='Hz')
        self.parameters['analyzer reference power'] = ConfigParameter(parent, value=0, unit='dBm')
        self.parameters['measure real input'] = ConfigParameter(parent, value=True, parameter_type='bool')
        self.parameters['Apply RF attenuation'] = ConfigParameter(parent, value=False, parameter_type='bool')
        self.parameters['RF attenuation'] = ConfigParameter(parent, value=4, unit='dBm')
        self.parameters['center frequency'] = ConfigParameter(parent, value=1e9, unit='Hz')
        self.parameters['frequency span'] = ConfigParameter(parent, value=1e6, unit='Hz')
        self.parameters['measure main tone frequencies'] = ConfigParameter(parent, value=True, parameter_type='bool')
        self.parameters['min power'] = ConfigParameter(parent, value=-10, unit='dBm')
        self.parameters['max power'] = ConfigParameter(parent, value=1, unit='dBm')
        self.parameters['power step'] = ConfigParameter(parent, value=0.5, unit='dBm')

        # frequency table data
        self._use_measured_frequencies_for_side_tones = False
        self.main_tone_source = CustomTableSource()
        self.main_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value='Name', cell_type='label'),
                           CustomTableCell(parent, cell_value='Set Point', cell_type='label'),
                           CustomTableCell(parent, cell_value='Measured', cell_type='label')))
        self.main_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value='f1', cell_type='label'),
                           CustomTableCell(parent, cell_type='float', unit='Hz', name='f1_setpoint'),
                           CustomTableCell(parent, cell_type='float', unit='Hz', name='f1_measured', is_enabled=False)))
        self.main_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value='f2', cell_type='label'),
                           CustomTableCell(parent, cell_type='float', unit='Hz', name='f2_setpoint'),
                           CustomTableCell(parent, cell_type='float', unit='Hz', name='f2_measured', is_enabled=False)))

        self.side_tone_source = CustomTableSource()
        self.side_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_type='empty'),
                           CustomTableCell(parent, cell_value='use measured tones', cell_type='label'),
                           CustomTableCell(parent, cell_value=False, cell_type='bool', name='use_measured_tones')))
        self.side_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value='Measure', cell_type='label'),
                           CustomTableCell(parent, cell_value='frequency', cell_type='label'),
                           CustomTableCell(parent, cell_value='Expected At', cell_type='label')))
        self.side_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value=True, cell_type='bool', name='enable_IM3Ord12'),
                           CustomTableCell(parent, cell_value='IM3Ord12', cell_type='label'),
                           CustomTableCell(parent, cell_type='float', name='set_IM3Ord12', unit='Hz',
                                           is_enabled=False)))
        self.side_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value=True, cell_type='bool', name='enable_IM3Ord21'),
                           CustomTableCell(parent, cell_value='IM3Ord21', cell_type='label'),
                           CustomTableCell(parent, cell_type='float', name='set_IM3Ord21', unit='Hz',
                                           is_enabled=False)))
        self.side_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value=True, cell_type='bool', name='enable_H2Ord1'),
                           CustomTableCell(parent, cell_value='H2Ord1', cell_type='label'),
                           CustomTableCell(parent, cell_type='float', name='set_H2Ord1', unit='Hz',
                                           is_enabled=False)))
        self.side_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value=True, cell_type='bool', name='enable_IM2Ord12'),
                           CustomTableCell(parent, cell_value='IM2Ord12', cell_type='label'),
                           CustomTableCell(parent, cell_type='float', name='set_IM2Ord12', unit='Hz',
                                           is_enabled=False)))
        self.side_tone_source.append(
            CustomTableRow(parent,
                           CustomTableCell(parent, cell_value=True, cell_type='bool', name='enable_H2Ord2'),
                           CustomTableCell(parent, cell_value='H2Ord2', cell_type='label'),
                           CustomTableCell(parent, cell_type='float', name='set_H2Ord2', unit='Hz',
                                           is_enabled=False)))

        # add dependency for side tone recalculation
        self.side_tone_source['use_measured_tones'].variable.trace('w', self._set_sidetones_)

        # setup dependency between frequency parameters and main tones
        self.parameters['center frequency'].variable.trace('w', self._set_tones_from_param_)
        self.parameters['frequency span'].variable.trace('w', self._set_tones_from_param_)
        self.main_tone_source['f1_setpoint'].variable.trace('w', self._set_param_from_tones_)
        self.main_tone_source['f2_setpoint'].variable.trace('w', self._set_param_from_tones_)
        self.main_tone_source['f1_measured'].variable.trace('w', self._frequency_measurement_finished_)
        self.main_tone_source['f2_measured'].variable.trace('w', self._frequency_measurement_finished_)
        self._frequency_update = False
        self._set_tones_from_param_()

        # definitions for commands
        self.commands = list()
        self.commands.append(ControlCommand(self.start, name='Run'))
        self.commands.append(ControlCommand(self.stop, name='Stop', can_execute=False))
        self.commands.append(ControlCommand(self.screenshot, name='Screenshot'))

        # results table
        self.result_source = CustomTableSource()
        self.result_source.append(CustomTableRow(parent,
                                                 CustomTableCell(parent, cell_type='empty'),
                                                 CustomTableCell(parent, cell_type='empty'),
                                                 CustomTableCell(parent, cell_type='empty'),
                                                 CustomTableCell(parent, cell_value='IM3Ord12 [dBm]', cell_type='label'),
                                                 CustomTableCell(parent, cell_value='f1 [dBm]', cell_type='label'),
                                                 CustomTableCell(parent, cell_value='f2 [dBm]', cell_type='label'),
                                                 CustomTableCell(parent, cell_value='IM3Ord21 [dBm]', cell_type='label'),
                                                 CustomTableCell(parent, cell_value='H2Ord1 [dBm]', cell_type='label'),
                                                 CustomTableCell(parent, cell_value='IM2Ord12 [dBm]', cell_type='label'),
                                                 CustomTableCell(parent, cell_value='H2Ord2 [dBm]', cell_type='label')))
        self.result_source.append(CustomTableRow(parent,
                                                 CustomTableCell(parent, cell_value='IIP3:', cell_type='label'),
                                                 CustomTableCell(parent, cell_type='float', name='res_IIP3', unit='dBm',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, cell_value='Min Power:', cell_type='label'),
                                                 CustomTableCell(parent, name='min_IM3Ord12', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='min_f1', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='min_f2', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='min_IM3Ord21', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='min_H2Ord1', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='min_IM2Ord12', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='min_H2Ord2', cell_type='float',
                                                                 is_enabled=False)))
        self.result_source.append(CustomTableRow(parent,
                                                 CustomTableCell(parent, cell_value='OIP3:', cell_type='label'),
                                                 CustomTableCell(parent, cell_type='float', name='res_OIP3', unit='dBm',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, cell_value='Max Power:', cell_type='label'),
                                                 CustomTableCell(parent, name='max_IM3Ord12', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='max_f1', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='max_f2', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='max_IM3Ord21', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='max_H2Ord1', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='max_IM2Ord12', cell_type='float',
                                                                 is_enabled=False),
                                                 CustomTableCell(parent, name='max_H2Ord2', cell_type='float',
                                                                 is_enabled=False)))

        self.custom_analysis_results_provider = CustomAnalysisResultProvider()
        self.custom_analysis_results_provider.IIP3 = self.result_source['res_IIP3']
        self.custom_analysis_results_provider.OIP3 = self.result_source['res_OIP3']
        self.custom_analysis_results_provider.min_IM3Ord12 = self.result_source['min_IM3Ord12']
        self.custom_analysis_results_provider.min_f1 = self.result_source['min_f1']
        self.custom_analysis_results_provider.min_f2 = self.result_source['min_f2']
        self.custom_analysis_results_provider.min_IM3Ord21 = self.result_source['min_IM3Ord21']
        self.custom_analysis_results_provider.min_H2Ord1 = self.result_source['min_H2Ord1']
        self.custom_analysis_results_provider.min_IM2Ord12 = self.result_source['min_IM2Ord12']
        self.custom_analysis_results_provider.min_H2Ord2 = self.result_source['min_H2Ord2']
        self.custom_analysis_results_provider.max_IM3Ord12 = self.result_source['max_IM3Ord12']
        self.custom_analysis_results_provider.max_f1 = self.result_source['max_f1']
        self.custom_analysis_results_provider.max_f2 = self.result_source['max_f2']
        self.custom_analysis_results_provider.max_IM3Ord21 = self.result_source['max_IM3Ord21']
        self.custom_analysis_results_provider.max_H2Ord1 = self.result_source['max_H2Ord1']
        self.custom_analysis_results_provider.max_IM2Ord12 = self.result_source['max_IM2Ord12']
        self.custom_analysis_results_provider.max_H2Ord2 = self.result_source['max_H2Ord2']

        # plot options
        self.plot_option_parameters = dict()
        self.plot_option_parameters['use defined interpolation interval'] = ConfigParameter(parent, value=True,
                                                                                            parameter_type='bool')
        self.plot_option_parameters['interpolation lower boundary'] = ConfigParameter(parent, value=-100, unit='dBm')
        self.plot_option_parameters['interpolation upper boundary'] = ConfigParameter(parent, value=-50, unit='dBm')
        self.plot_option_parameters['mark IIP2 point'] = ConfigParameter(parent, value=True, parameter_type='bool')
        self.plot_option_parameters['source file'] = ConfigParameter(parent, value=None, parameter_type='file')

        # experiment
        self.experiment = DemoExperiment()

        self.experiment_handler = ExperimentHandler()

        # listen if the experiment has been finished
        self.experiment_handler.experiment_finished.append(self._on_experiment_finished_)
        self.experiment_handler.current_experiment = self.experiment    # set the experiment in the handler
        self.plot_data = self.experiment.plot_collection

    def start(self):
        """
        Starts the experiment
        """
        print('start')
        self.screenshot(askpath=False)
        self.commands[0].can_execute = False    # disable the start button
        self.commands[1].can_execute = True     # enable the stop button
        self.enable_config.set(False)           # disable configuration on UI
        self.experiment.custom_analysis_options = self._get_custom_analysis_options_()
        self.experiment.plot_collection.clear()  # remove any old plots

        self.experiment_handler.run_experiment()    # run experiment in another thread

    def stop(self):
        """
        Stop the experiment manually.
        """
        print('stop')
        self.commands[0].can_execute = True     # enable the start button
        self.commands[1].can_execute = False    # disable the stop button
        self.enable_config.set(True)  # enable configuration on UI
        self.experiment_handler.stop_experiment()   # interrupt the experiment

    def screenshot(self, askpath=True):
        """Creates a screenshot of the user interface."""

        # built path name
        now = datetime.now()
        special_name = self.parameters['filename suffix'].value  # add to file name to identify quicker
        device_name = self.parameters['device name'].value
        base_path = self.parameters['out path'].value
        if base_path[-1] != '/': base_path += '/'
        screenshot_path = '{}_measurement_dev-{}_{}_{}-screenshot.png'.format(base_path, device_name,
                                                                              special_name,
                                                                              now.strftime('%Y-%m-%d_%H-%M-%S'))

        if askpath:     # ask for path
            result = filedialog.asksaveasfilename(initialdir=self.parameters['out path'].value)
            if result is None or result == '':
                return
            if result[-3:] != 'png': result += '.png'
            screenshot_path = result

        x, y = self._root.winfo_x(), self._root.winfo_y()   # capture window coordinates
        _capture_offset_x = 9   # x offset of window to coincide with screenshot
        _capture_offset_y = 32  # y offset of window to coincide with screenshot
        width, height = self._root.winfo_width(), self._root.winfo_height() # capture window dimensions
        # get screenshot
        im = grab(bbox=(x + _capture_offset_x, y,
                        x + width + _capture_offset_x, y + height + _capture_offset_y), childprocess=None)
        im.save(screenshot_path)    # save screenshot

    def apply_plot_changes(self):
        """
        Apply changes to main plot.
        """
        source_path = self.plot_option_parameters['source file'].value

        if source_path is None or not os.path.isfile(source_path):
            message('The specified file "{}" was not found.'.format(self.experiment.csv_path),
                    'File not found', message_type='error')
            return

    def _get_custom_analysis_options_(self):
        """Returns the custom analysis plot options based on the current settings on the UI."""
        return CustomAnalysisPlotOptions(self.plot_option_parameters['use defined interpolation interval'].value,
                                            self.plot_option_parameters['interpolation lower boundary'].value,
                                            self.plot_option_parameters['interpolation upper boundary'].value,
                                            self.plot_option_parameters['mark IIP2 point'].value)

    def on_shutdown(self):
        """
        Callback method which gets called once the application is trying to close.
        Before closing the application the currently running experiment is terminated.
        """
        self.experiment_handler.stop_experiment()

    def _set_tones_from_param_(self, *args):
        """
        If the frequency span or the center frequency were changed update the main frequencies
        in the frequencies tables.
        """
        if not self._frequency_update:  # lock the update mechanism during update
            self._frequency_update = True
            try:
                center = self.parameters['center frequency'].value
                span = self.parameters['frequency span'].value
                self.main_tone_source['f1_setpoint'].value = center - span / 2
                self.main_tone_source['f2_setpoint'].value = center + span / 2
                self.__set_sidetones__()    # update the side tone table
            except:
                pass
            self._frequency_update = False    # release the update mechanism

    def _set_param_from_tones_(self, *args):
        """
        If the main tones were changed in the frequency tables update the parameter table accordingly.
        """
        if not self._frequency_update:  # lock the update mechanism during update
            self._frequency_update = True
            try:
                f1 = self.main_tone_source['f1_setpoint'].value
                f2 = self.main_tone_source['f2_setpoint'].value
                self.parameters['center frequency'].value = (f1 + f2) / 2
                self.parameters['frequency span'].value = abs(f1 - f2)
                self._set_sidetones_()    # update the side tone table
            except:
                pass
            self._frequency_update = False    # release the update mechanism

    def _frequency_measurement_finished_(self, *args):
        """If the measured main tone frequencies changed during the experiment automatically recalculate the expected
        side tone frequencies based on the newly measured values."""
        self.side_tone_source['use_measured_tones'].value = True

    def _set_sidetones_(self, *args):
        """Sets the frequencies of the side tones in the frequency tables. This can be based on the set point values
        of the main tones or on the measured values."""
        if self.side_tone_source['use_measured_tones'].value:
            f1 = self.main_tone_source['f1_measured'].value
            f2 = self.main_tone_source['f2_measured'].value
        else:
            f1 = self.main_tone_source['f1_setpoint'].value
            f2 = self.main_tone_source['f2_setpoint'].value

        self.side_tone_source['set_IM3Ord12'].value = 2 * f1 - f2
        self.side_tone_source['set_IM3Ord21'].value = 2 * f2 - f1
        self.side_tone_source['set_H2Ord1'].value = 2 * f1
        self.side_tone_source['set_IM2Ord12'].value = f1 + f2
        self.side_tone_source['set_H2Ord2'].value = 2 * f2

    def _on_experiment_finished_(self):
        """Callback method which gets called once the experiment finishes"""
        self.commands[0].can_execute = True     # enable the start button
        self.commands[1].can_execute = False    # disable the stop button
        self.plot_option_parameters['source file'].value = self.experiment.csv_path
        self.enable_config.set(True)  # enable configuration on UI

    def _get_signal_source_devices(self):
        """Gets a list of potential signal source devices."""
        serial_ports = list_ports.comports()

        signal_generator_list = list()
        # add known network devices
        signal_generator_list.append('TCPIP0::ief-lab-psg70g-1.ee.ethz.ch::inst0::INSTR')
        signal_generator_list.append('TCPIP0::ief-lab-exg40g-1.ee.ethz.ch::inst0::INSTR')

        # add serial ports which are available at the computer
        for port in serial_ports:
            signal_generator_list.append(port.device)

        self.signal_generator_set = set(signal_generator_list)  # convert list to set (needed by tkinter)
