from dataclasses import dataclass
from enum import Enum
from typing import Callable
import numpy as np
from ..helpers.plots import ShapeDict
from matplotlib.patches import Rectangle
from shapely import Polygon


@dataclass
class Coord:
    x: float
    y: float

    def __getitem__(self, i):
        return (self.x, self.y)[i]

    @property
    def pair(self):
        return (self.x, self.y)


@dataclass
class Coordinate3D(Coord):
    z: float

    def get_pair(self, l1, l2):
        return Coord(self.__dict__[l1], self.__dict__[l2])


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

    @property
    def size(self):
        return self.max - self.min

    def buffered_min(self, val):
        return self.min + val * self.size

    def buffered_max(self, val):
        return self.max - val * self.size

    def midpoint(self):
        return (self.min + self.max) / 2

    def __eq__(self, other) -> bool:
        return np.isclose(self.min, other.min) and np.isclose(self.max, other.max)


@dataclass(frozen=True)
class Domain:
    horz_range: (
        Range  # TODO width is not an appropriate name, bc start and end matter..
    )
    vert_range: Range

    def get_dict_for_plotting(self, color="blue", label="") -> ShapeDict:
        return ShapeDict(
            type="rect",
            xref="x",
            yref="y",
            fillcolor=color,
            x0=self.horz_range.min,
            y0=self.vert_range.min,
            x1=self.horz_range.max,
            y1=self.vert_range.max,
            label=dict(text=label),
        )

    def get_mpl_patch(self):
        return Rectangle(
            (self.horz_range.min, self.vert_range.min),
            self.horz_range.size,
            self.vert_range.size,
            fill=False,
            edgecolor="black",
            alpha=0.2,
        )

    def create_coordinates(self):
        # following requirements for geomeppy block
        # ccw from bottom right
        br = (self.horz_range.max, self.vert_range.min)
        tr = (self.horz_range.max, self.vert_range.max)
        tl = (self.horz_range.min, self.vert_range.max)
        bl = (self.horz_range.min, self.vert_range.min)
        return [br, tr, tl, bl]

    def create_centroid(self):
        return Coord(self.horz_range.midpoint(), self.vert_range.midpoint())

    @property
    def area(self):
        return self.horz_range.size * self.vert_range.size

    @property
    def aspect_ratio(self):
        return self.horz_range.size / self.vert_range.size

    def get_shapely_rectangle(self):
        coords = self.create_coordinates()
        return Polygon(coords)

    @classmethod
    def from_coords_list(cls, coords: list[Coord]):
        xs = sorted(set([i.x for i in coords]))
        ys = sorted(set([i.y for i in coords]))
        horz_range = Range(xs[0], xs[-1])
        vert_range = Range(ys[0], ys[-1])
        return cls(horz_range, vert_range)

    # todo the extents should be here..


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


class WallNormal(Enum):
    # direction of outward normal of the wall..
    # https://eppy.readthedocs.io/en/latest/eppy.geometry.html#eppy.geometry.surface.azimuth
    NORTH = 0.0
    EAST = 90.0
    SOUTH = 180.0
    WEST = 270.0

    def __getitem__(self, i):
        return getattr(self, i)
