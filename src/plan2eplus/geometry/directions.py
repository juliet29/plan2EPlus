from enum import IntEnum
from typing import Literal


class WallNormal(IntEnum):  # TODO 6/2/25 -> possible breaking change
    # direction of outward normal of the wall..
    # https://eppy.readthedocs.io/en/latest/eppy.geometry.html#eppy.geometry.surface.azimuth
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270
    UP = 1
    DOWN = -1
    # TODO => if anything iterates over this it will throw an error

    def __getitem__(self, i):
        return getattr(self, i)

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())

WallNormalNames = Literal["NORTH", "EAST", "SOUT", "WEST", "UP", "DOWN"]