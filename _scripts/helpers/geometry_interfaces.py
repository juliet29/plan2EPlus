from dataclasses import dataclass
import numpy as np
from helpers.plots import ShapeDict
from matplotlib.patches import Rectangle

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
    width: Range
    height: Range

    def get_dict_for_plotting(self, color="blue", label="") -> ShapeDict:
        return ShapeDict(
        type="rect",
        xref="x",
        yref="y",
        fillcolor=color,
        x0=self.width.min,
        y0=self.height.min,
        x1=self.width.max,
        y1=self.height.max,
        label=dict(text=label),
    )

    def get_mpl_patch(self):
        return Rectangle((self.width.min, self.height.min), self.width.size, self.height.size, fill=False, edgecolor="black", alpha=0.2)

    def create_coordinates(self):
        # following requirements for geomeppy block
        # ccw from bottom right
        br = (self.width.max, self.height.min)
        tr = (self.width.max, self.height.max)
        tl = (self.width.min, self.height.max)
        bl = (self.width.min, self.height.min)
        return [br, tr, tl, bl]

    def create_centroid(self):
        return Coord(self.width.midpoint(), self.height.midpoint())
    
    @property
    def area(self):
        return self.width.size * self.height.size

    @property
    def aspect_ratio(self):
        return self.width.size / self.height.size



