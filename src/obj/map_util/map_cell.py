# Simon Chu
# Mon Jan 18 12:02:13 EST 2021

from src.obj.map_util.coord import Coord
from typing import Union, Optional


class Map_Cell:
    """
    Usage:
        >>> mc = Map_Cell(Coord(0, 1))
        >>> mc.x
        0
        >>> mc.y
        1
        >>> mc.set_attribute("visited", True)
        >>> mc.get_attribute("visited")
        True
        >>> mc.has_attribute("visited")
        True
    """
    def __init__(self, coord: Coord, attributes: Optional[dict[str, Union[int, float, bool]]] = None):
        self.coord_val = coord
        self.attributes_val = attributes

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
    def y(self, y):
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

    # def __eq__(self, other):
    #     if other is not None:
    #         return self.x == other.x and self.y == other.y
    #     else:
    #         return False
