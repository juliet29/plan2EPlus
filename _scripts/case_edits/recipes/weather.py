from gplan.room_class import GPLANRoomAccess
from case_edits.ezcase import EzCase, EzCaseInput
from geometry.wall import WallNormal
from outputs.variables import OutputVars as ov
from case_edits.recipes.two_zone import (
    PLAN_PATH,
    PLAN_INDEX,
    door_pairs,
    window_pairs,
    output_reqs,
)

TEST_CASE = "tests/test17_weather"
PLAN_PATH = "GPLANs/test.json"
PLAN_INDEX = 0


input = EzCaseInput(
    case_name=TEST_CASE,
    geometry=GPLANRoomAccess(PLAN_PATH, PLAN_INDEX),
    door_pairs=door_pairs,
    window_pairs=window_pairs,
    output_variables=output_reqs,
)
