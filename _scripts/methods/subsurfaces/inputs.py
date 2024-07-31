from dataclasses import dataclass
from munch import Munch
from typing import List, Sequence, Union
from geomeppy import IDF
from geomeppy.patches import EpBunch
from enum import Enum
from helpers.special_types import PairType
from methods.dynamic_subsurfaces.inputs import (
    Dimensions,
    NinePointsLocator,
)

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
class SubsurfaceInputs:
    zones: Munch
    ssurface_pairs: Sequence[PairType]
    case_idf: IDF
    attributes: (
        SubsurfaceAttributes  # TODO -> make into list of attributes corresponding to pair..
    )


@dataclass
class SurfaceGetterInputs:
    zones: Munch
    ssurface_pair: PairType
