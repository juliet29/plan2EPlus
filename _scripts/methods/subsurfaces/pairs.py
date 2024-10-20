from typing import Union
from new_subsurfaces.interfaces import (
    Dimensions,
)
from new_subsurfaces.interfaces import NinePointsLocator, SubsurfaceType
from new_subsurfaces.interfaces import SubsurfaceAttributes


DEFAULT_DOOR = SubsurfaceAttributes(
    object_type=SubsurfaceType.DOOR,
    construction=None,
    dimensions=Dimensions(0.3, 0.9),
    location_in_wall=NinePointsLocator.bottom_middle,
    FRACTIONAL=True,
)


DEFAULT_WINDOW = SubsurfaceAttributes(
    object_type=SubsurfaceType.WINDOW,
    construction=None,
    dimensions=Dimensions(0.3, 0.3),
    location_in_wall=NinePointsLocator.middle_middle,
    FRACTIONAL=True,
)
