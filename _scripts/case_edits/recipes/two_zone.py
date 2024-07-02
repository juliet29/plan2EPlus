from gplan.room_class import GPLANRoomAccess
from case_edits.ezcase import EzCase, EzCaseInput
from geometry.wall import WallNormal
from outputs.variables import OutputVars as ov

TEST_CASE = "tests/test16_ezcase"
PLAN_PATH = "GPLANs/test.json"
PLAN_INDEX = 0


door_pairs = [(0, WallNormal.NORTH), (0,1)]
window_pairs = [(1, WallNormal.SOUTH)]
output_reqs = [ov.zone_ach, ov.zone_mean_air_temp, ov.surf_net_thermal_rad]

input = EzCaseInput(case_name=TEST_CASE, geometry=GPLANRoomAccess(PLAN_PATH, PLAN_INDEX), door_pairs=door_pairs, window_pairs=window_pairs, output_variables=output_reqs)
ezcase = EzCase(input)