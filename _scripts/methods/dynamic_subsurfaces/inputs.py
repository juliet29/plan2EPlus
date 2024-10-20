from dataclasses import dataclass
from shapely import Point


class MutablePoint:
    # TODO not sure why this becoming numpy?
    def __init__(self, point: Point = None, x=None, y=None) -> None:
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
