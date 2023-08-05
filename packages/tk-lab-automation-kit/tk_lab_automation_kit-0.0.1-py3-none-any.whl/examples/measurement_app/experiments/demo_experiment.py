from tk_lab_automation_kit.experiments import Experiment, ExperimentHandler
from tk_lab_automation_kit.core import ObservableList
from tk_lab_automation_kit.user_interface import PlotData
from time import sleep
import numpy as np


class DemoExperiment(Experiment):

    def __init__(self):
        super().__init__()
        self.csv_path = 'res.csv'

    def run(self, handler: ExperimentHandler):
        self.plot_collection.clear()
        plot1 = PlotData(ObservableList(), ObservableList(), marker='.')
        plot2 = PlotData(ObservableList(), ObservableList(), linestyle='--')
        self.plot_collection.append(plot1)
        self.plot_collection.append(plot2)
        self.plot_collection[0].plot_control.show_grid = True

        x_range = np.linspace(0, 5*np.pi)

        for x in x_range:
            plot1.x.append(x)
            plot1.y.append(np.sin(x))
            plot2.x.append(x)
            plot2.y.append(np.cos(x))
            sleep(0.05)