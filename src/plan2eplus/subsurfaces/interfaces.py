from dataclasses import dataclass
from enum import Enum
from typing import Literal, NamedTuple

from plan2eplus.geometry.range import Dimensions
from ..geometry.directions import WallNormal
from eppy.bunch_subclass import EpBunch


class SubsurfaceObjects(Enum):
    DOOR = 0
    WINDOW = 1


# SubsurfaceObjects = Literal["DOOR" | "WINDOW"]


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
    object_type: SubsurfaceObjects  # TODO whey couldnt this be a literal?
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
