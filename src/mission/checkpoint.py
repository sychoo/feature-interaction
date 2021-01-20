# Simon Chu
# Mon Jan 18 12:45:10 EST 2021

from src.obj.map import Coord, Map, Map_Cell
from src.obj.drone import Drone
from src.obj.visualizer import Visualizer
from stl.api import Signal, STL
from typing import Tuple, Optional


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
        self._map: Optional[Map] = None
        self._ego_drone: Optional[Drone] = None
        self._chaser_drone: Optional[Drone] = None

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
        self._ego_drone = Drone(id="Ego", map=self._map, init_loc=self._map.map_cell(self.ego_init_loc))
        self._chaser_drone = Drone(id="Chaser", map=self._map, init_loc=self._map.map_cell(self.chaser_init_loc))

    def state_planner(self, ego_curr_cell: Map_Cell, chaser_curr_cell: Map_Cell, ego_heading: Coord) -> Tuple[
        Map_Cell, Map_Cell]:
        """given the current state (location) of the ego and chaser drone, and the heading of ego drone, predict the next state (location)

        Specifically, find the neighbor that maximally advance towards the heading coordinate

        chaser drone will be using outdated information when analysing the maximal advancement

        the state_predictor will make sure chaser and ego remain in their current position when no advancement can be made
        """
        ###################################################
        # neighbor cells for ego drones and chaser drones #
        ###################################################

        ego_neighbor_cells: list[Map_Cell] = self._map.neighbor(ego_curr_cell)
        chaser_neighbor_cells: list[Map_Cell] = self._map.neighbor(chaser_curr_cell)

        max_ego_advancement = 0  # default ego drone advancement value
        max_ego_advancement_neighbor_cell = ego_curr_cell  # default ego advancement to ego_curr_cell

        ##########################################################################
        # advance ego drone first make it as close to the checkpoint as possible #
        ##########################################################################

        for curr_ego_neighbor_cell in ego_neighbor_cells:
            ego_neighbor_d2h = curr_ego_neighbor_cell.distance_to(
                self._map.map_cell(ego_heading))  # neighbor distance to heading
            ego_curr_d2h = ego_curr_cell.distance_to(self._map.map_cell(ego_heading))  # ego distance to heading
            advancement = ego_curr_d2h - ego_neighbor_d2h

            if advancement > max_ego_advancement:
                max_ego_advancement = advancement
                max_ego_advancement_neighbor_cell = curr_ego_neighbor_cell

        ###############################
        # advance chaser drone second #
        ###############################

        max_chaser_advancement = 0  # default ego drone advancement value
        max_chaser_advancement_neighbor_cell = chaser_curr_cell  # default ego advancement to ego_curr_cell

        # advance ego drone first
        for curr_chaser_neighbor_cell in chaser_neighbor_cells:
            chaser_neighbor_d2e = curr_chaser_neighbor_cell.distance_to(
                ego_curr_cell)  # chaser distance to (old) ego loc
            chaser_curr_d2e = chaser_curr_cell.distance_to(ego_curr_cell)  # chaser distance to heading
            advancement = chaser_curr_d2e - chaser_neighbor_d2e

            if advancement > max_chaser_advancement:
                max_chaser_advancement = advancement
                max_chaser_advancement_neighbor_cell = curr_chaser_neighbor_cell

        return max_ego_advancement_neighbor_cell, max_chaser_advancement_neighbor_cell

    # TODO: predict, execute (loop refer to flight.py in old repo)
    def signal_predictor(self, ego_heading: Coord, pred_step: int) -> Tuple[
        Signal, Signal]:  # return ego_drone_pred_signal, chaser_drone_pred_signal
        """predict/estimate the future signal based on the current signals (represent information like heading (coord)
        in hidden class varibles self._heading
        @:param step: the number of steps the predictor need to predict
        """
        pred_signal_ego = Signal()
        pred_signal_chaser = Signal()

        # append the current state of the drone to the first index of the predictive signal for consistency
        pred_signal_ego.append(py_dict={"x": self._ego_drone.loc.x, "y": self._ego_drone.loc.y})
        pred_signal_chaser.append(py_dict={"x": self._chaser_drone.loc.x, "y": self._chaser_drone.loc.y})

        curr_ego_loc = self._ego_drone.loc
        curr_chaser_loc = self._chaser_drone.loc

        for i in range(pred_step):
            curr_ego_loc, curr_chaser_loc = self.state_planner(ego_curr_cell=curr_ego_loc,
                                                               chaser_curr_cell=curr_chaser_loc,
                                                               ego_heading=ego_heading)
            pred_signal_ego.append(py_dict={"x": curr_ego_loc.x, "y": curr_ego_loc.y})
            pred_signal_chaser.append(py_dict={"x": curr_chaser_loc.x, "y": curr_chaser_loc.y})

        return pred_signal_ego, pred_signal_chaser

    # TODO: start the execution loop, figure out a way to share data between drones, and use the STL_API to evaluate the properties defined.
    # TODO: Generate messages to display on the matplotlib grap
    def execute(self, max_step=30, pred_step=4, prop: Optional[list[STL]] = None) -> Tuple[
        list[Tuple[str, Signal, list[Signal]]], list[str]]:
        """simulate runtime of the drone
        @:param max_step: the maximum step allowed (in case of infinite loop)
        @:param pred_signal: length of each predictive signal generated
        @:param prop: properties to be check via the STL tool and the predictive signals

        return the exe_signal and list of pred_signals for ego drone and chaser drone, respectively
        invoke STL and predict function
        """
        #####################################################################################
        # init the signal accumulators, message list record state info for initial location #
        #####################################################################################
        exe_signal_ego: Signal = Signal()
        exe_signal_chaser: Signal = Signal()

        pred_signals_ego: list[Signal] = list()
        pred_signals_chaser: list[Signal] = list()

        # append initial location to the execution signals
        exe_signal_ego.append(py_dict={"x": self.ego_init_loc.x, "y": self.ego_init_loc.y})
        exe_signal_chaser.append(py_dict={"x": self.chaser_init_loc.x, "y": self.chaser_init_loc.y})

        messages = list()

        ################################################
        # start the execution cycle, record state info #
        ################################################
        for curr_heading in self.checkpoints:
            while self._ego_drone.loc.coord != curr_heading:  # the ego drone has not reached the current heading

                ###########################################
                # predict the signal via signal predictor #
                ###########################################

                # TODO: estimate pred_step length-ed signal
                pred_signal_ego, pred_signal_chaser = self.signal_predictor(ego_heading=curr_heading,
                                                                            pred_step=pred_step)
                pred_signals_ego.append(pred_signal_ego)
                pred_signals_chaser.append(pred_signal_chaser)

                ####################################################################
                # predict feature conflicts in signals via STL-API, update message #
                ####################################################################
                # RESEARCH TODO: partial feature interaction for multiple features satisficement
                # TODO: define properties in the def prop(self):, pass it into start() function
                # TODO: modify STL-API, type check and evaluation (robustness/satisfaction) for logical operators
                # G[0, pred_step](0 < x < map_width && 0 < y < map_height)
                bound_prop_list = list()
                bound_prop_list.append(
                    STL("G[0, " + str(pred_step) + "](x < " + str(self.map_width - 3) + ")"))  # boundary property
                bound_prop_list.append(
                    STL("G[0, " + str(pred_step) + "](y < " + str(self.map_height - 3) + ")"))  # boundary property
                bound_prop_list.append(STL("G[0, " + str(pred_step) + "](x > 3)"))  # boundary property
                bound_prop_list.append(STL("G[0, " + str(pred_step) + "](y > 3)"))  # boundary property

                message = "\n"
                min_robustness_ego = 100
                satisfy_ego = True

                # ego drone satisfaction and robustness
                for prop in bound_prop_list:
                    prop_eval = prop.eval(0, pred_signal_ego)
                    if not prop_eval.satisfy:
                        satisfy_ego = False
                    if prop_eval.robustness < min_robustness_ego:
                        min_robustness_ego = prop_eval.robustness

                if not satisfy_ego:
                    message += "EGO CRASHING rob.     =  " + str(int(min_robustness_ego)) + "\n"
                else:
                    message += "                           \n"

                min_robustness_chaser = 100
                satisfy_chaser = True

                # chaser drone satisfaction and robustness
                for prop in bound_prop_list:
                    prop_eval = prop.eval(0, pred_signal_chaser)
                    if not prop_eval.satisfy:
                        satisfy_chaser = False
                    if prop_eval.robustness < min_robustness_chaser:
                        min_robustness_chaser = prop_eval.robustness

                if not satisfy_chaser:
                    message += "CHASER CRASHING rob. =" + str(int(min_robustness_chaser))
                else:
                    message += "                       \n"

                # if messages is not "":
                if satisfy_ego and satisfy_chaser:
                    message = "no conflict. rob.  =" + str(min(min_robustness_chaser, min_robustness_ego))

                messages.append(message)

                # TODO: python math library support for operations, syntactic sugar support || -> abs
                # TODO: support evaluation of two signals (via parameter passing) or aggregate the signals into one with grouping (ego.x, ego.y, chaser.x, chaser.y)
                # G[0, pred_step](sqrt(x^2 + y^2)|
                # G[0, pred_step]((x - y)^2
                # d2c_prop =  STL("G[")  # distance to chaser drone property

                ##########################################
                # execution runtime, determine next step #
                ##########################################
                ego_next_cell, chaser_next_cell = self.state_planner(ego_curr_cell=self._ego_drone.loc,
                                                                     chaser_curr_cell=self._chaser_drone.loc,
                                                                     ego_heading=curr_heading)

                # set the new coordinates for the drones
                self._ego_drone.loc = ego_next_cell
                self._chaser_drone.loc = chaser_next_cell

                exe_signal_ego.append(py_dict={"x": ego_next_cell.x, "y": ego_next_cell.y})
                exe_signal_chaser.append(py_dict={"x": chaser_next_cell.x, "y": chaser_next_cell.y})

                if max_step <= 0:  # case when the execution exceed the allowed max_step
                    break
                max_step -= 1

            if max_step <= 0:
                break

        # append placeholder predictive signal to enforce consistency
        pred_signal_ego = Signal()
        pred_signal_ego.append(py_dict={"x": self._ego_drone.loc.x, "y": self._ego_drone.loc.y})

        pred_signal_chaser = Signal()
        pred_signal_chaser.append(py_dict={"x": self._chaser_drone.loc.x, "y": self._chaser_drone.loc.y})

        pred_signals_ego.append(pred_signal_ego)
        pred_signals_chaser.append(pred_signal_chaser)

        # append placeholder message
        messages.append("\nExecution Complete!!!!!!!!\n            ")
        ############################################
        # return aggregated list for visualization #
        ############################################

        print(exe_signal_ego)
        print(exe_signal_chaser)
        return [(self._ego_drone.id, exe_signal_ego, pred_signals_ego),
                (self._chaser_drone.id, exe_signal_chaser, pred_signals_chaser)], messages

    def start(self):
        """start the simulation and visualize the signal data"""
        self.init()  # init essential objects
        signal_data, messages = self.execute()  # start simulation runtime/execution, obtain resulting signal
        visual = Visualizer(width=self.map_width, height=self.map_height, signal_data=signal_data, messages=messages)  # init visualizer
        visual.show()  # start visualizer
