# Thu Jan 14 13:43:49 EST 2021
# from stl.api import Signal

from stl.api import Signal


class Visualizer:
    def __init__(self, exe_signal: Signal, pred_signals: list[Signal]):
        """
        initialize 2D signal visualizer, note that signal must have x and y entry
        :param exe_signal: the executing signal
        :param pred_signals: a list of predictive signals at every step during the execution of the drone
        """
        self.exe_signal_val = exe_signal
        self.pred_signals_val = pred_signals

    @property
    def exe_signal(self):
        return self.exe_signal_val

    @exe_signal.setter
    def exe_signal(self, exe_signal):
        self.exe_signal_val = exe_signal

    @property
    def pred_signals(self):
        return self.pred_signals_val
