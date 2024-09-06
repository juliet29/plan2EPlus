from copy import deepcopy

from case_edits.ezcase import EzCaseInput
from methods.subsurfaces.pairs import SubsurfacePair as SSP
from methods.subsurfaces.pairs import SubsurfaceObjects
from methods.subsurfaces.pairs import DEFAULT_WINDOW
from geometry.wall_normal import WallNormal


from gplan.room_class import GPLANRoomAccess
from gplan.subsurfaces import SubsurfaceTranslator
from case_edits.ezcase import EzCaseInput
from recipes.two_zone import output_reqs

TEST_CASE = "tests/test21_amber"
PLAN_DIR = "amber_a"
PLAN_INDEX = 0

st = SubsurfaceTranslator("amber_a")
st.run()


input = EzCaseInput(
    case_name=TEST_CASE,
    geometry=GPLANRoomAccess(st.gplan_path, PLAN_INDEX),
    subsurface_pairs=(st.door_pairs + st.window_pairs),
    output_variables=output_reqs,
)