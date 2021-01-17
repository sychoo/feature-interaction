# Thu Jan 14 13:43:49 EST 2021
# from stl.api import Signal
# visualize the execution path and the predictive signals based on the signal and identifier provided.

from stl.api import Signal
from typing import Tuple, Union, Optional
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

ANIMATION_REFRESH_INTERVAL = 400  # time between the animation is refreshed


class Visualizer:
    """
    Signal Format:
    {
        "0": {
            "content": {
                "x": 1,
                "y": 2
                ...
            }
        },
        "1": {
            "content": {
                "x": 2,
                "y": 1
                ...
            }
        }
    }

    Note that the signal uses x and y to represent the coordinate system
    signal_data_val: [(id_1: str, exe_signal_1: Signal, pred_signals_1: list[Signal]), (id_2, exe_signal_2: Signal, pred_signals_2: list[Signal]), ...]
    """

    def __init__(self, signal_data: list[Tuple[str, Signal, list[Signal]]] = list(),
                 width: Optional[int] = None,
                 height: Optional[int] = None):  # initialize a fresh new list
        """
        initialize 2D signal visualizer, note that signal must have x and y entry
        """
        self.signal_data_val = signal_data
        self.width_val = width
        self.height_val = height
        self._counter = 0  # initialize the counter to 0, count the steps into the animation

    def append(self, id_val: str, exe_signal: Signal, pred_signals: list[Signal]) -> None:
        """append (execution signal, predictive signal) pairs to the signal data
        :param id_val: the identifier of the signals
        :param exe_signal: the executing signal
        :param pred_signals: a list of predictive signals at every step during the execution of the drone
        """
        self.signal_data_val.append((id_val, exe_signal, pred_signals))

    #######################
    # getters and setters #
    #######################
    @property
    def width(self) -> Optional[int]:
        return self.width_val

    @width.setter
    def width(self, width: int):
        self.width_val = width

    @property
    def height(self) -> Optional[int]:
        return self.height_val

    @height.setter
    def height(self, height: int):
        self.height_val = height

    def __len__(self):
        return len(self.id_list)

    @property
    def id_list(self) -> list[str]:
        """signal id list """
        return list(map(lambda tuple_val: tuple_val[0], self.signal_data_val))

    @property
    def exe_signal_list(self) -> list[Signal]:
        """execution signal list"""
        return list(map(lambda tuple_val: tuple_val[1], self.signal_data_val))

    @property
    def pred_signal_lists(self) -> list[list[Signal]]:
        """predicted signal lists"""
        return list(map(lambda tuple_val: tuple_val[2], self.signal_data_val))

    def init(self) -> None:
        plt.style.use('fivethirtyeight')  # use style excerpted from fivethirtyeight.com

        plt.xticks(np.arange(0, self.width, 1.0))  # set x axis increment to 1
        plt.yticks(np.arange(0, self.height, 1.0))  # set y axis increment to 1
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom=False, bottom=False, top=False,
                        labeltop=True, length=0)

        # ax.lines = [exe_line_1, pred_line_1, exe_line_2, pred_line_2]
        for id_val in self.id_list:  # put the id as labels on the graph
            plt.plot([], [], label=id_val)  # drone exe signal label
            plt.plot([], [], label=id_val + " Prediction", linestyle="dashed")  # drone pred signal label

        ax = plt.gca()  # get and set current axis instances
        ax.set_xlim(0, self.width)
        ax.set_ylim(self.height, 0)

        plt.legend()  # display the legend
        plt.tight_layout()  # use tight_layout

        # the # of lines should be 2x the # of id/labels
        assert len(ax.lines) == 2 * len(self)

    # TODO: equivalent to animate_helper
    def animate(self, _):
        # print("counter: " + str(self._counter))  # debug

        ax = plt.gca()

        for idx in range(0, len(self)):
            exe_line = ax.lines[idx * 2]  # the line for show execution signal of the drone
            pred_line = ax.lines[idx * 2 + 1]  # the line for the predictive signal of the drone

            exe_signal: Signal = self.exe_signal_list[idx]  # the execution signal corresponding to the line
            pred_signals: list[Signal] = self.pred_signal_lists[
                idx]  # the predictive signal corresponding to the line

            assert len(exe_signal) == len(pred_signals)

            if self._counter < len(exe_signal):  # prevent accessing signal elements that are out of bound
                curr_exe_signal_begin = 0
                curr_exe_signal_end = self._counter
                curr_exe_signal: Signal = exe_signal.get(curr_exe_signal_begin, curr_exe_signal_end)  # slice signals
                curr_pred_signal: Signal = pred_signals[self._counter]

                # linearize signals Signal -> [x_cor_1, x_cor_2, ...], [y_cor_1, y_cor_2, ...]
                linearized_curr_exe_signal_x, linearized_curr_exe_signal_y = self.linearize_signal(curr_exe_signal)
                linearized_curr_pred_signal_x, linearized_curr_pred_signal_y = self.linearize_signal(curr_pred_signal)

                exe_line.set_data(linearized_curr_exe_signal_x, linearized_curr_exe_signal_y)
                pred_line.set_data(linearized_curr_pred_signal_x, linearized_curr_pred_signal_y)

                # print(linearized_curr_exe_signal_x)
                # print(linearized_curr_exe_signal_y)
                # print(linearized_curr_pred_signal_x)
                # print(linearized_curr_pred_signal_y)

        self._counter += 1

    @staticmethod
    def linearize_signal(signal: Signal) -> Tuple[list[int], list[int]]:
        # TODO: function to linearized given signal to tuple of x coordinates and y coordinates
        return signal.lookup("x"), signal.lookup("y")

    def start_animation(self):
        print("starting animation")  # debug
        animation = FuncAnimation(plt.gcf(), self.animate, interval=ANIMATION_REFRESH_INTERVAL)  # gcf: get curr figure
        plt.show()

    def show(self):
        self.init()
        self.start_animation()
