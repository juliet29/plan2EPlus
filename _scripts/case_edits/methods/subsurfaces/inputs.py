from dataclasses import dataclass
from munch import Munch
from typing import List, Tuple
from geomeppy import IDF
from geomeppy.patches import EpBunch
from enum import Enum

DOOR_GAP = 2/100 #m 


class SubsurfaceType(Enum):
    DOOR = 0
    WINDOW = 1

@dataclass
class SubsurfaceAttributes:
    type:SubsurfaceType 
    length:int
    height:int
    construction:EpBunch

@dataclass
class SubsurfaceInputs:
    zones: Munch
    ssurface_pairs: List[Tuple]
    case_idf: IDF
    attributes: SubsurfaceAttributes #TODO -> list of attributes corresponding to pair..

@dataclass
class SurfaceGetterInputs:
    zones: Munch
    ssurface_pair:Tuple
