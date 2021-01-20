# Simon Chu
# Mon Jan 18 12:04:21 EST 2021

from src.obj.map_util.coord import Coord
from src.obj.map_util.map_cell import Map_Cell
from math import sqrt


class Map:
    """encapsulate the map information. represented by a 1D array holding Map_Cell objects

    Usage:
        >>> m = Map(5, 10)
        >>> m.width
        5
        >>> m.height
        10
    """
    def __init__(self, width, height):
        self.width_val = width
        self.height_val = height
        self.map_array_val = list()

        # flattens the 2D array to 1D, from left to right (increment x_cor, then increment y_cor)
        for y in range(height):
            for x in range(width):
                new_map_cell = Map_Cell(Coord(x, y))
                self.map_array_val.append(new_map_cell)

    #######################
    # getters and setters #
    #######################

    @property
    def width(self):
        return self.width_val

    @width.setter
    def width(self, width: int):
        self.width_val = width

    @property
    def height(self):
        return self.height_val

    @height.setter
    def height(self, height: int):
        self.height_val = height

    @property
    def map_array(self):
        return self.map_array_val

    @map_array.setter
    def map_array(self, map_array: list):
        self.map_array_val = map_array

    @property
    def diagonal_length(self) -> float:
        """diagonal length of the map"""
        return sqrt(self.width_val ** 2 + self.height_val ** 2)

    def map_cell(self, coord: Coord):
        """obtain the map cell from the map"""
        if not self.check_bound(coord):
            raise RuntimeError("index out of bound, unable to obtain map cell")

        # convert 2D array index to flattened 1D array index
        converted_index = (self.width * coord.y) + coord.x
        return self.map_array_val[converted_index]

    def check_bound(self, coord: Coord):
        """check whether the coord is within the map boundaries"""
        return (0 <= coord.x < self.width) and (0 <= coord.y < self.height)

    def neighbor(self, map_cell: Map_Cell) -> list[Map_Cell]:
        # TODO: implement in neighbor the algorithm, append "north" "south" labels in the def neighbor_dict(map_cell):
        """obtain a list of neighbor map_cells"""
        return list(self.find_neighbors_8(map_cell).values())

    def find_neighbors_8(self, map_cell: Map_Cell) -> dict[str, Map_Cell]:
        neighbor_dict = dict()

        x_cor = map_cell.x
        y_cor = map_cell.y

        new_x_cor = x_cor
        new_y_cor = y_cor - 1
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["north"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor
        new_y_cor = y_cor + 1
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["south"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor + 1
        new_y_cor = y_cor
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["east"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor - 1
        new_y_cor = y_cor
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["west"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor + 1
        new_y_cor = y_cor - 1
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["northeast"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor + 1
        new_y_cor = y_cor + 1
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["southeast"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor - 1
        new_y_cor = y_cor + 1
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["southwest"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor - 1
        new_y_cor = y_cor - 1
        if self.check_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["northwest"] = self.map_cell(Coord(new_x_cor, new_y_cor))

        return neighbor_dict

    def print_map_array(self):
        """visualize the internal maps (containing x and y coordinate and the output value)"""

        for index, map_cell in enumerate(self.map_array_val):
            if index % self.width == 0:
                print("height = " + str(map_cell.y))

            print(map_cell)

            if index % self.width == self.width - 1:
                print()

    # TODO: visualize attributes? def print_attribute("visited"):
    # def visualize_visited_map(self):
    #     # visualize the map if the map contains "map" attribute
    #     for row_array in self.get_visited_map():
    #         print("\t", end="")
    #
    #         for element in row_array:
    #             print("{0:2}".format(element), end="")
    #
    #         print()
    #
    # def visualize_output_map(self):
    #     # visualize the map if the map contains "map" attribute
    #     for row_array in self.get_output_map():
    #         print("\t", end="")
    #
    #         for element in row_array:
    #             print("{0:2}".format(element), end="")
    #
    #         print()
    #
    #
