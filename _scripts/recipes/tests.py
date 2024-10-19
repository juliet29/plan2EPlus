from plan.room_class import GPLANRoomAccess
from case_edits.ezcase import EzCaseInput
from geometry.wall_normal import WallNormal
from outputs.variables import OutputVars as ov
from recipes.two_zone import (
    PLAN_PATH,
    PLAN_INDEX,
    door_pairs,
    window_pairs,
    output_reqs,
)

TEST_CASE = "tests/test18_many_windows"

window_pairs.append((1, WallNormal.EAST))
window_pairs.append((1, WallNormal.WEST))
# window_pairs.append((0, WallNormal.WEST))
window_pairs.append((0, WallNormal.EAST))
# window_pairs.append((0, WallNormal.SOUTH)) # cant do because there are many south surfaces => future work ..

input = EzCaseInput(
    case_name=TEST_CASE,
    geometry=GPLANRoomAccess(PLAN_PATH, PLAN_INDEX),
    door_pairs=door_pairs,
    window_pairs=window_pairs,
    output_variables=output_reqs,
)
