# Simon Chu
# Mon Jan 18 12:00:56 EST 2021
from math import sqrt


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

    @property
    def neighbor(self) -> list['Coord']:
        """return list of 8 neighbors around the coordinates"""
        result = [
            Coord(self.x - 1, self.y - 1),
            Coord(self.x - 1, self.y),
            Coord(self.x - 1, self.y + 1),
            Coord(self.x, self.y - 1),
            Coord(self.x, self.y + 1),
            Coord(self.x + 1, self.y - 1),
            Coord(self.x + 1, self.y),
            Coord(self.x + 1, self.y + 1)
        ]

        return result

    def distance_to(self, other: 'Coord') -> float:
        """calculate the distance between 2 coordinates"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __eq__(self, other):
        if other is not None:
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __str__(self):
        return "Coord: ( " + str(self.x) + ", " + str(self.y) + " )"
