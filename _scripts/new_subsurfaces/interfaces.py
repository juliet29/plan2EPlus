from dataclasses import dataclass
from enum import Enum

from geometry.wall_normal import WallNormal
from methods.dynamic_subsurfaces.inputs import Dimensions, NinePointsLocator

from geomeppy.patches import EpBunch


class SubsurfaceType(Enum):
    DOOR = 0
    WINDOW = 1


@dataclass
class SubsurfaceAttributes:
    object_type: SubsurfaceType
    construction: EpBunch | None
    dimensions: Dimensions
    location_in_wall: NinePointsLocator
    FRACTIONAL: bool = False
    SHADING: bool = False


class SubsurfacePair:
    def __init__(
        self, space_a: int, space_b: int | WallNormal, attrs: SubsurfaceAttributes
    ) -> None:
        self.space_a = space_a
        self.space_b = space_b
        self.attrs = attrs

    def __repr__(self) -> str:
        return f"SSP(pair={self.space_a, self.space_b}, type={self.attrs.object_type.name}, dims=({self.attrs.dimensions.width}, {self.attrs.dimensions.height})"
