from copy import deepcopy

 
from case_edits.ezcase import EzCaseInput
from geometry.wall_normal import WallNormal
from outputs.variables import OutputVars as ov
from new_subsurfaces.interfaces import SubsurfacePair as SSP
from methods.subsurfaces.pairs import DEFAULT_WINDOW

TEST_CASE = "tests/test16_ezcase"
PLAN_PATH = "GPLANs/test.json"
PLAN_INDEX = 0

shade_window = deepcopy(DEFAULT_WINDOW)
shade_window.SHADING = True
window_pairs = [SSP(1, WallNormal.SOUTH, shade_window), 
                SSP(1, WallNormal.EAST, shade_window)
                ]

door_pairs = [SSP(0, WallNormal.NORTH), SSP(0, 1)]
# for d in door_pairs:
#     d.attrs = DEFAULT_DOOR
subsurface_pairs = door_pairs + window_pairs

output_reqs = [
    ov.zone_ach,
    ov.zone_mean_air_temp,
    ov.surf_net_thermal_rad,
    ov.node_temp,
    ov.node_total_pressure,
    ov.node_wind_pressure,
    ov.linkage_flow12,
    ov.linkage_flow21,
    ov.surface_venting,
    ov.site_wind_speed,
    ov.site_wind_direction,
    ov.surf_inside_temp,
    ov.zone_vent_heat_gain,
    ov.zone_vent_heat_loss,
    ov.surf_outside_temp,
    ov.surf_incident_solar_rad,
]

input = EzCaseInput(
    case_name=TEST_CASE,
    geometry=GPLANRoomAccess(PLAN_PATH, PLAN_INDEX),
    subsurface_pairs=subsurface_pairs,
    output_variables=output_reqs,
)
# ezcase = EzCase(input)
