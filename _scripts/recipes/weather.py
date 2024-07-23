from gplan.room_class import GPLANRoomAccess
from case_edits.ezcase import EzCaseInput
from geometry.wall import WallNormal
from outputs.variables import OutputVars as ov
from recipes.two_zone import (
    PLAN_PATH,
    PLAN_INDEX,
    door_pairs,
    window_pairs,
    output_reqs,
)

TEST_CASE = "tests/test17_weather"

window_pairs.append((1, WallNormal.EAST))

input = EzCaseInput(
    case_name=TEST_CASE,
    geometry=GPLANRoomAccess(PLAN_PATH, PLAN_INDEX),
    door_pairs=door_pairs,
    window_pairs=window_pairs,
    output_variables=output_reqs,
)
