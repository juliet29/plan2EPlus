from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Callable, NamedTuple
import numpy as np
from ..helpers.plots import ShapeDict
from matplotlib.patches import Rectangle
from shapely import Polygon
from plan2eplus.helpers.helpers import dataclass_as_dict

# TODO organize classes -> dunder methods, then class methods, then properties, then other things..


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

    @property
    def midpoint(self):
        return (self.min + self.max) / 2

    def __eq__(self, other) -> bool:
        return np.isclose(self.min, other.min) and np.isclose(self.max, other.max)


@dataclass
class CoordList:
    # sample_coords: int = 0

    @property
    def asdict(self) -> dict[str, Coord]:
        return dataclass_as_dict(self)

    @property
    def as_pairs_dict(self):  # TOOD use a dict here..
        return {k: v.pair for k, v in self.asdict.items()}

    @property
    def as_pairs(self):  # TOOD use a dict here..
        return [v.pair for v in self.asdict.values()]
        # return [self.north.pair, self.south.pair, self.west.pair, self.east.pair]


# TODO potentially pair w/ card directions?
@dataclass
class PerimeterMidpoints(CoordList):
    north: Coord
    south: Coord
    east: Coord  
    west: Coord




@dataclass
class Bounds(CoordList):
    br: Coord
    tr: Coord
    tl: Coord
    bl: Coord


def extend_bounds(bounds:Bounds, EXTENTS:int):
    br = (bounds.br.x + EXTENTS, bounds.br.y - EXTENTS)
    tr = (bounds.tr.x + EXTENTS, bounds.tr.y + EXTENTS)
    tl = (bounds.tl.x - EXTENTS, bounds.tl.y + EXTENTS)
    bl = (bounds.bl.x - EXTENTS), bounds.bl.y - EXTENTS
    coords = [br, tr, tl, bl]
    return Bounds(*[Coord(*i) for i in coords])




@dataclass(frozen=True)
class Domain:
    horz_range: Range
    vert_range: Range

    @classmethod
    def from_coords_list(cls, coords: list[Coord]): 
        # TODO can it be > 4 coords? 
        xs = sorted(set([i.x for i in coords]))
        ys = sorted(set([i.y for i in coords]))
        horz_range = Range(xs[0], xs[-1])
        vert_range = Range(ys[0], ys[-1])
        return cls(horz_range, vert_range)
    
    @classmethod
    def from_perimeter_mid_points(cls, pm:PerimeterMidpoints):
        horz_range = Range(pm.west.x, pm.east.x)
        vert_range = Range(pm.south.y, pm.north.y)
        return cls(horz_range, vert_range)
    
    @classmethod
    def from_bounds(cls, bounds:Bounds):
        horz_range = Range(bounds.tl.x, bounds.tr.x)
        vert_range = Range(bounds.bl.y, bounds.tl.y)
        return cls(horz_range, vert_range)

    @property
    def centroid(self):
        return Coord(self.horz_range.midpoint, self.vert_range.midpoint)

    @property
    def area(self):
        return self.horz_range.size * self.vert_range.size

    @property
    def aspect_ratio(self):
        return self.horz_range.size / self.vert_range.size

    def create_bounds(self, EXTENTS=0):  # TODO should be a property..
        # following requirements for geomeppy block
        # ccw from bottom right
        br = (self.horz_range.max, self.vert_range.min)
        tr = (self.horz_range.max, self.vert_range.max)
        tl = (self.horz_range.min, self.vert_range.max)
        bl = (self.horz_range.min, self.vert_range.min)

        coords = [br, tr, tl, bl]
        init_bounds = Bounds(*[Coord(*i) for i in coords])

        if not EXTENTS:
            return init_bounds
        
        return extend_bounds(init_bounds, EXTENTS)


    def create_perimeter_midpoints(self, EXTENTS=0):
        north = (self.horz_range.midpoint, self.vert_range.max + EXTENTS)
        south = (self.horz_range.midpoint, self.vert_range.min - EXTENTS)
        east = (self.horz_range.max + EXTENTS, self.vert_range.midpoint)
        west = (self.horz_range.min - EXTENTS, self.vert_range.midpoint)
        coords = [north, south, east, west]

        return PerimeterMidpoints(*[Coord(*i) for i in coords]) # TODO potentially extract the extension here also 

    # TODO should be in a seperate class devoted to graphing.. 
    def get_mpl_patch(self):
        return Rectangle(
            (self.horz_range.min, self.vert_range.min),
            self.horz_range.size,
            self.vert_range.size,
            fill=False,
            edgecolor="black",
            alpha=0.2,
        )

    # todo the extents should be here.. as a separate multi domain object..
@dataclass
class MultiDomain:
    domains: list[Domain]

    @property
    def total_domain(self):
        min_x = min([i.horz_range.min for i in self.domains]) 
        max_x = max([i.horz_range.max for i in self.domains]) 
        min_y = min([i.vert_range.min for i in self.domains]) 
        max_y = max([i.vert_range.max for i in self.domains]) 
        return Domain(Range(min_x, max_x), Range(min_y, max_y))
    
    @property
    def external_coord_positions(self):
        return self.total_domain.create_perimeter_midpoints(EXTENTS=1)
    
    @property
    def extended_domain_with_external_coords(self):
        external_coords_domain = Domain.from_perimeter_mid_points(self.external_coord_positions)
        extended_bounds = external_coords_domain.create_bounds(EXTENTS=1)
        return Domain.from_bounds(extended_bounds)
    






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

    # def __lt__(self):
    #     return
