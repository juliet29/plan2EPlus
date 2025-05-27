from copy import deepcopy
import pytest

from plan2eplus.case_edits.ezcase import create_ezcase
from plan2eplus.helpers.ep_geom_helpers import WallNormal
from plan2eplus.param.param import SurfaceMapping, apply_modifications
from plan2eplus.plan.graph_to_subsurfaces import Dimensions
from plan2eplus.subsurfaces.interfaces import NinePointsLocator, SubsurfaceAttributes, SubsurfaceObjects


@pytest.fixture
def bolinas_case():
    inputs_dir = "case_bol_5"
    outputs_dir = "test/test25_airwwall"
    return create_ezcase(outputs_dir, inputs_dir)

def test_apply_subsurface_modifications(bolinas_case):
    assert bolinas_case
    ## try with new attributes 
    ## TODO then later think about modifying the attributes that exist in Bolinas
    ## need to map out fully though and think about the primary use cases.. 
    ns_windows = SubsurfaceAttributes(SubsurfaceObjects.WINDOW, construction=None, dimensions=Dimensions(0.1, 0.1), location_in_wall=NinePointsLocator.middle_middle)
    ew_windows = deepcopy(ns_windows).dimensions = Dimensions(0.2, 0.1)
    idf = apply_modifications(bolinas_case.idf, [ns_windows, ew_windows], mapping=SurfaceMapping.NS_EW)
    ## now need to check if the walls are as would be expected.. 

    exterior_walls = [i for i in idf.getsurfaces() if i.Outside_Boundary_Condition == "outdoors" and i.Surface_Type == "wall"]

    north_walls = [i for i in exterior_walls if WallNormal(round(float(i.azimuth))) == WallNormal.NORTH]
    east_walls = [i for i in exterior_walls if WallNormal(round(float(i.azimuth))) == WallNormal.EAST]

    # extended idf will have the subsurface map..
    for wall in north_walls:
        assert bolinas_case.surface_mappings[wall.Name] == ns_windows
    for wall in east_walls:
        assert bolinas_case.surface_mappings[wall.Name] == ew_windows
    # and need to clarfify the process... 

