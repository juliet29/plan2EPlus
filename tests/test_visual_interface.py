from plan2eplus.constants import DEFAULT_IDF_NAME, PATH_TO_DUMMY_OUTPUTS
from plan2eplus.case_edits.epcase import read_existing_idf
from plan2eplus.helpers.ep_geom_helpers import WallNormal
from plan2eplus.helpers.ep_helpers import get_zones
from plan2eplus.visuals.interfaces import Surface, Zone

EXPECTED_N_ZONES = 4  # TODO redundant with test_graphbem!


def test_create_idf_from_saved_data():
    case = read_existing_idf(PATH_TO_DUMMY_OUTPUTS)
    zones = get_zones(case.idf)
    assert len(zones) == EXPECTED_N_ZONES


def test_create_surface_geometry_object():
    case = read_existing_idf(PATH_TO_DUMMY_OUTPUTS)
    surface_name = "Block 00 `corner_ventilation` Storey 0 Roof 0001"
    surface = Surface.create(case.idf, surface_name)
    assert surface.direction == WallNormal.UP

def test_create_zone_object():
    case = read_existing_idf(PATH_TO_DUMMY_OUTPUTS)
    zone_name = "Block 00 `corner_ventilation` Storey 0"
    zone = Zone.create(case.idf, zone_name)
    assert zone.dname.zone_number == 0
