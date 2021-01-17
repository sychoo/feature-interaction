from src.obj.visualizer import Visualizer
from stl.api import Signal


# demonstrate visualizer
# exe_signal goes from 0, 0 to 5, 5, with each step increment by 1
# pred_signal simply goes 3 steps horizontally to the right
# --- (1)
#  --- (2)
#   --- (3)
#    --- (4)
#     --- (5)
#      --- (6)

def main():
    # create execution and predictive signals
    total_steps = 6  # number of total steps for the execution
    exe_signal: Signal = Signal()
    pred_signals: list[Signal] = list()

    # create placeholder signals for predictive signals
    for _ in range(total_steps):
        pred_signals.append(Signal())

    # add specific coordinates to signals
    for coord in range(total_steps):
        exe_signal.append(py_dict={"x": coord, "y": coord})
        pred_signals[coord].append(py_dict={"x": coord, "y": coord})
        pred_signals[coord].append(py_dict={"x": coord + 1, "y": coord})
        pred_signals[coord].append(py_dict={"x": coord + 2, "y": coord})
        pred_signals[coord].append(py_dict={"x": coord + 3, "y": coord})

    print(exe_signal)
    print(pred_signals)

    visual = Visualizer(width=10, height=10)
    visual.append("Ego Drone", exe_signal, pred_signals)
    visual.show()


# if __name__ == "__main__":
main()
