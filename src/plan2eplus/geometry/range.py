from dataclasses import dataclass
from enum import Enum
from typing import Callable, Literal, NamedTuple
import numpy as np


from ..helpers.plots import ShapeDict


class InvalidRangeException(Exception):
    def __init__(self, min, max) -> None:
        super().__init__(self)
        print(f"{min:.2f} cannot be less than {max:.2f}")


@dataclass(frozen=True)
class Range:
    min: float
    max: float

    def __post_init__(self):
        try:
            assert self.min <= self.max
        except AssertionError:
            raise InvalidRangeException(self.min, self.max)

    def __repr__(self) -> str:
        return f"[{self.min:.2f}, {self.max:.2f}]"

    def __eq__(self, other) -> bool:
        return np.isclose(self.min, other.min) and np.isclose(self.max, other.max)

    @property
    def as_tuple(self):
        return (self.min, self.max)

    @property
    def midpoint(self):
        return (self.min + self.max) / 2

    @property
    def size(self):
        return self.max - self.min

    def buffered_min(self, val):
        return self.min + val * self.size

    def buffered_max(self, val):
        return self.max - val * self.size

        # return [self.north.pair, self.south.pair, self.west.pair, self.east.pair]

    # @classmethod
    # def from_list_of_coords(cls, coords:list[Coord]):



@dataclass
class Dimensions:  # TODO why is this different from a Domain?
    width: float
    height: float

    def __getitem__(self, i):
        return (self.width, self.height)[i]

    @property
    def area(self):
        return self.width * self.height

    def modify(self, fx: Callable[[float], float]):
        return self.__class__(fx(self.width), fx(self.height))

    def modify_area(self, factor: float):
        # preserves aspect ratio
        sqrt_val = factor ** (1 / 2)
        return self.__class__.modify(self, lambda x: sqrt_val * x)


# TODO -> convert these to be associated with the EPBUnch, https://eppy.readthedocs.io/en/latest/_modules/eppy/bunch_subclass.html#addfunctions


# def __lt__(self):
#     return
