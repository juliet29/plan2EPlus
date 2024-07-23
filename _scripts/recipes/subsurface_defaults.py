from case_edits.methods.subsurfaces.inputs import SubsurfaceInputs, SubsurfaceAttributes, SubsurfaceObjects
from case_edits.methods.dynamic_subsurfaces.inputs import (
    Dimensions,
    NinePointsLocator,
)

# TODO: default constructions.. 

DEFAULT_DOOR = SubsurfaceAttributes(
    object_type=SubsurfaceObjects.DOOR, 
    construction=None,
    dimensions=Dimensions(0.3, 0.9),
    location_in_wall=NinePointsLocator.bottom_middle,
    FRACTIONAL=True
)


DEFAULT_WINDOW = SubsurfaceAttributes(
    object_type=SubsurfaceObjects.WINDOW, 
    construction=None,
    dimensions=Dimensions(0.3, 0.3),
    location_in_wall=NinePointsLocator.middle_middle,
    FRACTIONAL=True
)