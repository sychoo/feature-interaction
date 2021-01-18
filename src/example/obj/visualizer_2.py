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

    ################################
    # create signals for ego drone #
    ################################

    exe_signal_ego: Signal = Signal()
    pred_signals_ego: list[Signal] = list()

    # create placeholder signals for predictive signals
    for _ in range(total_steps):
        pred_signals_ego.append(Signal())

    # add specific coordinates to signals
    for coord in range(total_steps):
        exe_signal_ego.append(py_dict={"x": coord, "y": coord})
        pred_signals_ego[coord].append(py_dict={"x": coord, "y": coord})
        pred_signals_ego[coord].append(py_dict={"x": coord + 1, "y": coord})
        pred_signals_ego[coord].append(py_dict={"x": coord + 2, "y": coord})
        pred_signals_ego[coord].append(py_dict={"x": coord + 3, "y": coord})

    # print(exe_signal_ego)
    # print(pred_signals_ego)

    ###################################
    # create signals for chaser drone #
    ###################################

    exe_signal_chaser: Signal = Signal()
    pred_signals_chaser: list[Signal] = list()

    # create placeholder signals for predictive signals
    for _ in range(total_steps):
        pred_signals_chaser.append(Signal())

    # add specific coordinates to signals
    for coord in range(total_steps):
        exe_signal_chaser.append(py_dict={"x": 10 - coord, "y": 10 - coord})
        pred_signals_chaser[coord].append(py_dict={"x": 10 - coord, "y": 10 - coord})
        pred_signals_chaser[coord].append(py_dict={"x": 9 - coord, "y": 10 - coord})
        pred_signals_chaser[coord].append(py_dict={"x": 8 - coord, "y": 10 - coord})
        pred_signals_chaser[coord].append(py_dict={"x": 7 - coord, "y": 10 - coord})

    # print(exe_signal_chaser)
    # print(pred_signals_chaser)

    ##########################
    # create global messages #
    ##########################

    messages = list()
    for i in range(total_steps):
        if i % 2 == 0:  # case when i is even, No Conflict
            messages.append("No Conflict")
        else:
            messages.append("Conflict Detected")


    ############################
    # initiated the visualizer #
    ############################

    visual = Visualizer(width=10, height=10, messages=messages)
    visual.append("Ego Drone", exe_signal_ego, pred_signals_ego)
    visual.append("Chaser Drone", exe_signal_chaser, pred_signals_chaser)
    visual.show()


# if __name__ == "__main__":
main()
