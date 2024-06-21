from dataclasses import dataclass
from munch import Munch
from typing import List, Sequence
from geomeppy import IDF
from geomeppy.patches import EpBunch
from enum import Enum
from case_edits.special_types import PairType

DOOR_GAP = 2 / 100  # m


class SubsurfaceObjects(Enum):
    DOOR = 0
    WINDOW = 1


@dataclass
class SubsurfaceAttributes:
    object_type: SubsurfaceObjects
    length: int
    height: int
    construction: EpBunch


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
