
from dataclasses import dataclass
from typing import Union
from geometry.wall_normal import WallNormal
from geomeppy.patches import EpBunch
from enum import Enum
from methods.dynamic_subsurfaces.inputs import (
    Dimensions,
    NinePointsLocator,
)



class SubsurfaceObjects(Enum):
    DOOR = 0
    WINDOW = 1

@dataclass
class SubsurfaceAttributes:
    object_type: SubsurfaceObjects
    construction: Union[EpBunch, None]
    dimensions: Dimensions
    location_in_wall: NinePointsLocator
    FRACTIONAL: bool = False
    SHADING: bool = False


DEFAULT_DOOR = SubsurfaceAttributes(
    object_type=SubsurfaceObjects.DOOR,
    construction=None,
    dimensions=Dimensions(0.3, 0.9),
    location_in_wall=NinePointsLocator.bottom_middle,
    FRACTIONAL=True,
)


DEFAULT_WINDOW = SubsurfaceAttributes(
    object_type=SubsurfaceObjects.WINDOW,
    construction=None,
    dimensions=Dimensions(0.3, 0.3),
    location_in_wall=NinePointsLocator.middle_middle,
    FRACTIONAL=True,
)


class SubsurfacePair:
    def __init__(self, space_a: int, space_b: Union[int, WallNormal], attrs: Union[SubsurfaceAttributes, SubsurfaceObjects] = SubsurfaceObjects.DOOR) -> None:
        self.space_a = space_a
        self.space_b = space_b
        self.attrs = attrs
        self.set_default_attrs()

    def set_default_attrs(self):
        if type(self.attrs) == SubsurfaceObjects:
            if self.attrs == SubsurfaceObjects.DOOR:
                self.attrs = DEFAULT_DOOR
            elif self.attrs == SubsurfaceObjects.WINDOW:
                self.attrs = DEFAULT_WINDOW

    def __repr__(self) -> str:
        return(
            f"SubsurfacePair(pair={self.space_a, self.space_b}, type={self.attrs.object_type})"
        )
            

        
