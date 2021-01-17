# Simon Chu
# Created: Tue Oct  6 22:28:12 EDT 2020
# Modified: Sun Jan 17 14:53:30 EST 2021
# support map operations
import math
from typing import Union, Optional

class Coord:
    """encapsulate 2D cooridnates information

    Usage:
        >>> coord = Coord(1, 2)
        >>> coord.x
        1
        >>> coord.y
        2
    """
    def __init__(self, x: int, y: int):
        self.x_val = x  # x coordinate
        self.y_val = y  # y coordinate

    #######################
    # getters and setters #
    #######################
    @property
    def x(self):
        return self.x_val

    @x.setter
    def x(self, x: int):
        self.x_val = x

    @property
    def y(self):
        return self.y_val

    @y.setter
    def y(self, y: int):
        self.y_val = y

    def distance_to(self, other: 'Coord') -> float:
        """calculate the distance between 2 coordinates"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __str__(self):
        return "Coord: ( " + str(self.x) + ", " + str(self.y) + " )"


class Map_Cell:
    """
    Usage:
        >>> mc = Map_Cell(Coord(0, 1))
    """
    def __init__(self, coord: Coord, attributes: Optional[dict[str, Union[int, float, bool]]] = None):
        self.coord_val = coord
        self.attributes_val = attributes  # Python dictionary, stores different attribute/property about the heatmap cells

    #######################
    # getters and setters #
    #######################
    @property
    def coord(self):
        return self.coord_val

    @coord.setter
    def coord(self, coord: Coord):
        self.coord_val = coord

    @property
    def attributes(self):
        return self.attributes_val

    @attributes.setter
    def attributes(self, attributes: dict[str, Union[int, float, bool]]):
        self.attributes_val = attributes

    @property
    def x(self):
        return self.coord_val.x

    @x.setter
    def x(self, x):
        self.coord_val.x = x

    @property
    def y(self) -> int:
        return self.coord_val.y

    @y.setter
    def y(self, y) -> int:
        self.coord_val.y = y

    def set_attribute(self, key: str, value: Union[int, float, bool]):
        self.attributes[key] = value

    def get_attribute(self, key: str) -> Optional[Union[int, float, bool]]:
        """get attribute via key, return None if attribute doesn't exist"""
        if self.has_attribute(key):
            return self.attributes[key]
        else:
            return None

    def has_attribute(self, key) -> bool:
        """check if an attribute exists in the dictionary"""
        return key in self.attributes.keys()

    def distance_to(self, other: 'Map_Cell') -> float:
        return self.coord.distance_to(other.coord)

    def __str__(self):
        return "Map Cell: ( " + str(self.x) + ", " + str(self.y) + " )"


# Map object represent the map, and consist of a list of Map_Cells
# TODO: refactor the code below
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # initialize a 1-D array that contains MapCells
        self.internal_map = []

        # this data structure flattens the 2D array to 1D, from left to right (increment x_cor, then increment y_cor)
        for y in range(height):
            for x in range(width):
                new_map_cell = Map_Cell(Coord(x, y))
                self.internal_map.append(new_map_cell)

        # debug
        # for i in self.internal_map:
        #     print("(" + str(i.get_x_cor()) + " , " + str(i.get_y_cor()) + ")")

        # print(self.internal_map)
    @property
    def width(self):
        return self.width_val

    def get_diagonal_length(self):
        return math.sqrt(self.width ** 2 + self.width ** 2)

    def get_flattened_internal_map(self):
        if hasattr(self, "internal_map"):
            return self.internal_map
        else:
            raise RuntimeError("map variable has not been initialized.")

    def get_output(self, coord):
        return self.get_map_cell(coord).get_output()

    def set_output(self, coord, output):
        self.get_map_cell(coord).set_output(output)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    # def get_map_cell(self, x_index, y_index):
    def get_map_cell(self, coord):
        # check the range for the x and y index
        if self.check_index_bound(coord):
            pass
        else:
            raise RuntimeError("index out of bound, unable to obtain map cell")

        # translate 2D array index to flattened 1D array index
        transformed_index = coord.y() * self.width + coord.x()
        return self.internal_map[transformed_index]

    def check_index_bound(self, coord):
        # check whether the x and y index is within the bound of the map
        return coord.x() >= 0 and coord.x() < self.width and coord.y() >= 0 and coord.y() < self.height

    def get_output_map(self):
        # generate the output map for seaborn (after manipulating the special output variable)
        return [[self.get_map_cell(Coord(x, y)).get_output() for x in range(self.width)] for y in range(self.height)]

    def get_visited_map(self):
        # generate the output map for seaborn (after manipulating the special output variable)
        return [[self.get_map_cell(Coord(x, y)).get_visited() for x in range(self.width)] for y in range(self.height)]

    def find_neighbors_8(self, map_cell):
        neighbor_dict = {}

        x_cor = map_cell.x()
        y_cor = map_cell.y()

        new_x_cor = x_cor
        new_y_cor = y_cor - 1
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["north"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor
        new_y_cor = y_cor + 1
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["south"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor + 1
        new_y_cor = y_cor
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["east"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor - 1
        new_y_cor = y_cor
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["west"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor + 1
        new_y_cor = y_cor - 1
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["northeast"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor + 1
        new_y_cor = y_cor + 1
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["southeast"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor - 1
        new_y_cor = y_cor + 1
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["southwest"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        new_x_cor = x_cor - 1
        new_y_cor = y_cor - 1
        if self.check_index_bound(Coord(new_x_cor, new_y_cor)):
            neighbor_dict["northwest"] = self.get_map_cell(Coord(new_x_cor, new_y_cor))

        return neighbor_dict

    def visualize_internal_map(self):
        # visualize the internal maps (containing x and y coordinate and the output value)

        # check whether the internal_map attribute has been initialized in the Map object
        if hasattr(self, "internal_map"):
            for index, map_cell in enumerate(self.internal_map):
                if index % self.width == 0:
                    print("height = " + str(map_cell.y()))

                print(map_cell)

                if index % self.width == self.width - 1:
                    print()
        else:
            raise RuntimeError("map variable has not been initialized.")

    def visualize_visited_map(self):
        # visualize the map if the map contains "map" attribute
        for row_array in self.get_visited_map():
            print("\t", end="")

            for element in row_array:
                print("{0:2}".format(element), end="")

            print()

    def visualize_output_map(self):
        # visualize the map if the map contains "map" attribute
        for row_array in self.get_output_map():
            print("\t", end="")

            for element in row_array:
                print("{0:2}".format(element), end="")

            print()


