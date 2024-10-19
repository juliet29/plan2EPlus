from copy import deepcopy

from case_edits.ezcase import EzCaseInput
from methods.subsurfaces.pairs import SubsurfacePair as SSP
from methods.subsurfaces.pairs import SubsurfaceObjects
from methods.subsurfaces.pairs import DEFAULT_WINDOW
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
        SSP(1,WallNormal.NORTH, SubsurfaceObjects.WINDOW), 
        SSP(5,1, SubsurfaceObjects.DOOR), 
        SSP(4,5, SubsurfaceObjects.DOOR), 
        SSP(4,WallNormal.SOUTH, SubsurfaceObjects.WINDOW)])

    return input

# _window = deepcopy(DEFAULT_WINDOW)
# shaded_window.SHADING = True


shaded_window = deepcopy(DEFAULT_WINDOW)
shaded_window.SHADING = True


def ns_axis_shaded(input:EzCaseInput):
    input.subsurface_pairs.extend([
        SSP(1,WallNormal.NORTH, shaded_window), 
        SSP(5,1, SubsurfaceObjects.DOOR), 
        SSP(4,5, SubsurfaceObjects.DOOR), 
        SSP(4,WallNormal.SOUTH, shaded_window)])

    return input