from plan2eplus.geometry.directions import WallNormal
from plan2eplus.helpers.ep_helpers import get_zones
from plan2eplus.visuals.interfaces import Surface, Zone


def test_create_idf_from_saved_data(defaults, test_case):
    _, EXPECTED_N_ZONES = defaults
    zones = get_zones(test_case.idf)
    assert len(zones) == EXPECTED_N_ZONES


def test_create_surface_geometry_object(test_case):
    surface_name = "Block 00 `a` Storey 0 Roof 0001"
    surface = Surface.create(test_case.idf, surface_name)
    assert surface.direction == WallNormal.UP


def test_create_zone_object(test_case):
    zone_name = "Block 00 `a` Storey 0"
    zone = Zone.create(test_case.idf, zone_name)
    assert zone.dname.zone_number == 0
