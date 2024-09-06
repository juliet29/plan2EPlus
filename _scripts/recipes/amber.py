from copy import deepcopy

from case_edits.ezcase import EzCaseInput
from methods.subsurfaces.pairs import SubsurfacePair as SSP
from methods.subsurfaces.pairs import SubsurfaceObjects
from methods.subsurfaces.pairs import DEFAULT_WINDOW
from geometry.wall_normal import WallNormal


from gplan.room_class import GPLANRoomAccess
from case_edits.ezcase import EzCaseInput
from recipes.two_zone import output_reqs

TEST_CASE = "tests/test21_amber"
PLAN_PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/outputs/amber_a/gplan.json"
PLAN_INDEX = 0

input = EzCaseInput(
    case_name=TEST_CASE,
    geometry=GPLANRoomAccess(PLAN_PATH, PLAN_INDEX),
    subsurface_pairs=[],
    output_variables=output_reqs,
)