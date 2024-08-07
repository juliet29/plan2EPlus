from dataclasses import dataclass
from munch import Munch
from typing import List, Union
from geomeppy import IDF

from methods.subsurfaces.pairs import SubsurfacePair



@dataclass
class SubsurfaceCreatorInputs:
    zones: Munch
    ssurface_pairs: List[SubsurfacePair]
    case_idf: IDF


@dataclass
class SurfaceGetterInputs:
    zones: Munch
    ssurface_pair: SubsurfacePair
