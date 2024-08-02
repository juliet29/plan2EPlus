from dataclasses import dataclass
from munch import Munch
from typing import List, Sequence, Union
from enum import Enum

from geomeppy import IDF
from geomeppy.patches import EpBunch

from helpers.special_types import PairType
from methods.dynamic_subsurfaces.inputs import (
    Dimensions,
    NinePointsLocator,
)
from geometry.wall import WallNormal


DOOR_GAP = 2 / 100  # m


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


@dataclass
class SubsurfacePair:
    space_a: int
    space_b: Union[int, WallNormal]  # can be an adjoiining zone, or a direction
    attrs: Union[SubsurfaceAttributes, None] = None
    # eventually will perhaps read off of a connectivity graph like JPG..


@dataclass
class SubsurfaceCreatorInputs:
    zones: Munch
    ssurface_pairs: Sequence[SubsurfacePair]
    case_idf: IDF


@dataclass
class SurfaceGetterInputs:
    zones: Munch
    ssurface_pair: SubsurfacePair
