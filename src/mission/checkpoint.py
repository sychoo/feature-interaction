# Simon Chu
# Mon Jan 18 12:45:10 EST 2021

from src.obj.map import Coord, Map
from src.obj.drone import Drone
from src.obj.visualizer import Visualizer
from stl.api import Signal
from typing import Tuple


class Checkpoint_Mission:
    """class to support the checkpoint mission"""
    def __init__(self,
                 map_width: int,
                 map_height: int,
                 ego_init_loc: Coord,
                 chaser_init_loc: Coord,
                 checkpoints: list[Coord]):
        self.map_width_val = map_width
        self.map_height_val = map_height
        self.ego_init_loc_val = ego_init_loc
        self.chaser_init_loc_val = chaser_init_loc
        self.checkpoints_val = checkpoints

        # initialize all internal objects to None
        self._map = None
        self._ego_drone = None
        self._chaser_drone = None


    ###########
    # getters #
    ###########

    @property
    def map_width(self):
        return self.map_width_val

    @property
    def map_height(self):
        return self.map_height_val

    @property
    def ego_init_loc(self):
        return self.ego_init_loc_val

    @property
    def chaser_init_loc(self):
        return self.chaser_init_loc_val

    @property
    def checkpoints(self):
        return self.checkpoints_val

    # TODO: initalize essential objects, like drones, maps, etc.
    def init(self) -> None:
        """initialize essential objects"""
        self._map = Map(width=self.map_width, height=self.map_height)
        self._ego_drone = Drone("Ego")
        self._chaser_drone = Drone("Enemy")

    # TODO: predict, execute (loop refer to flight.py in old repo)
    def predict(self, step: int) -> Tuple[Signal, Signal]:  # return ego_drone_pred_signal, chaser_drone_pred_signal
        """predict/estimate the future signal based on the current signals (represent information like heading (coord)
        in hidden class varibles self._heading
        """
        pass

    # TODO: start the execution loop, figure out a way to share data between drones, and use the STL_API to evaluate the properties defined.
    # TODO: Generate messages to display on the matplotlib grap
    def execute(self) -> list[Tuple[str, Signal, list[Signal]]]:
        """simulate runtime of the drone
        return the exe_signal and list of pred_signals for ego drone and chaser drone, respectively
        invoke STL and predict function
        """
        pass

    def start(self):
        """start the simulation and visualize the signal data"""
        self.init()  # init essential objects
        signal_data = self.execute()  # start simulation runtime/execution, obtain resulting signal
        visual = Visualizer(width=self.map_width, height=self.map_height, signal_data=signal_data)  # init visualizer
        visual.show()  # start visualizer



