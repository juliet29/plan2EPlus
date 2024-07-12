from dataclasses import dataclass
from enum import Enum
from shapely import Point


@dataclass
class Dimensions:
    width: float
    height: float


class MutablePoint:
    #TODO not sure why this becoming numpy? 
    def __init__(self, point:Point=None, x=None, y=None) -> None:
        if not point:
            self.x = float(x)
            self.y = float(y)
        else:
            self.x = float(point.x)
            self.y = float(point.y)
        # self.point = Point(self.x, self.y)

    def update_vals(self, x=None, y=None):
        if x is not None:
            self.x = float(x)

        if y is not None:
            self.y = float(y)

    def __repr__(self) -> str:
        return f"MutablePoint({self.x, self.y})"

        # self.point = Point(self.x, self.y)

@dataclass
class NinePoints:
    top_left: Point
    top_middle: Point
    top_right: Point

    middle_left: Point
    middle_middle: Point
    middle_right: Point

    bottom_left: Point
    bottom_middle: Point
    bottom_right: Point


class NinePointsLocator(Enum):
    top_left = 0
    top_middle = 1
    top_right = 2

    middle_left = 3
    middle_middle = 4
    middle_right = 5

    bottom_left = 6
    bottom_middle = 7
    bottom_right = 8