from copy import deepcopy

from case_edits.ezcase import EzCaseInput
from methods.subsurfaces.pairs import SubsurfacePair as SSP
from methods.subsurfaces.pairs import SubsurfaceObjects
from methods.subsurfaces.pairs import DEFAULT_DOOR
from geometry.wall_normal import WallNormal


from plan.room_class import GPLANRoomAccess
from case_edits.ezcase import EzCaseInput
from recipes.two_zone import output_reqs

TEST_CASE = "tests/test17_exp01"
PLAN_PATH = "GPLANs/ostwald_plans.json"
PLAN_INDEX = 0

input = EzCaseInput(
    case_name=TEST_CASE,
    geometry=GPLANRoomAccess(PLAN_PATH, PLAN_INDEX),
    subsurface_pairs=[],
    output_variables=output_reqs,
)

def ns_axis(input:EzCaseInput):
    input.subsurface_pairs.extend([
        SSP(1,WallNormal.NORTH, SubsurfaceObjects.DOOR), 
        SSP(5,WallNormal.NORTH, SubsurfaceObjects.DOOR), 
        SSP(4,WallNormal.NORTH, SubsurfaceObjects.DOOR), 
        SSP(4,WallNormal.SOUTH, SubsurfaceObjects.DOOR)])

    return input


def ew_axis(input:EzCaseInput):
    input.subsurface_pairs.extend([
        SSP(5,WallNormal.WEST, SubsurfaceObjects.DOOR), 
        SSP(5,WallNormal.EAST, SubsurfaceObjects.DOOR), 
        SSP(2,WallNormal.EAST, SubsurfaceObjects.DOOR)])

    return input

def cross_axis(input:EzCaseInput):
    input = ns_axis(input)
    input = ew_axis(input)
    return input


shaded_door = deepcopy(DEFAULT_DOOR)
shaded_door.SHADING = True

def shaded_exterior(input:EzCaseInput):
    input.subsurface_pairs.extend([
    SSP(1,WallNormal.NORTH, shaded_door), 
    SSP(5,WallNormal.NORTH, SubsurfaceObjects.DOOR), 
    SSP(4,WallNormal.NORTH, SubsurfaceObjects.DOOR), 
    SSP(4,WallNormal.SOUTH, shaded_door)])
    
    input.subsurface_pairs.extend([
    SSP(5,WallNormal.WEST, shaded_door), 
    SSP(5,WallNormal.EAST, SubsurfaceObjects.DOOR),
    SSP(2,WallNormal.EAST, shaded_door)])
    return input
