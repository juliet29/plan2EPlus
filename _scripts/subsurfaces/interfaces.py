from dataclasses import dataclass
from enum import Enum
from typing import Callable, NamedTuple
from helpers.ep_helpers import WallNormal
from eppy.bunch_subclass import EpBunch


class SubsurfaceObjects(Enum):
    DOOR = 0
    WINDOW = 1


@dataclass
class Dimensions:
    width: float
    height: float

    def __getitem__(self, i):
        return (self.width, self.height)[i]
    
    @property
    def area(self):
        return self.width * self.height
    

    def modify(self, fx:Callable[[float], float]):
        return self.__class__(fx(self.width), fx(self.height))
    
    def modify_area(self, factor:float):
        # preserves aspect ratio 
        sqrt_val = factor**(1/2)
        return self.__class__.modify(self, lambda x: sqrt_val*x)

    

    
    



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


@dataclass
class SubsurfaceAttributes:
    object_type: SubsurfaceObjects
    construction: EpBunch | None
    dimensions: Dimensions
    location_in_wall: NinePointsLocator
    FRACTIONAL: bool = False
    SHADING: bool = False


class SubsurfacePair:
    def __init__(
        self,
        space_a: int | WallNormal,
        space_b: int | WallNormal,
        attrs: SubsurfaceAttributes,
    ) -> None:
        self.space_a = space_a
        self.space_b = space_b
        self.attrs = attrs

    def __repr__(self) -> str:
        return f"SSP(pair={self.space_a, self.space_b}, type={self.attrs.object_type.name}, dims=({self.attrs.dimensions.width}, {self.attrs.dimensions.height})"


class PairOnly(NamedTuple):
    space_a: int
    space_b: WallNormal | int
