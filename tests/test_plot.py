from typing import Literal, NamedTuple

import pytest

from plan2eplus.geometry.directions import WallNormal
from plan2eplus.helpers.ep_helpers import get_zones
from plan2eplus.visuals.edge_coords import (
    find_points_along_path,
    sort_zone_and_facade_list,
)
from plan2eplus.visuals.interfaces import PlanZones, Zone
from plan2eplus.visuals.plot import plot_zone_domains


def test_plot_zone_domains(test_case):
    # test_case = read_existing_idf(path_class.models / TEST_CASE)
    plan_zones = PlanZones(test_case.idf)
    plot_zone_domains(plan_zones)
    assert 1  # just checking that doesnt throw any errors for now..


def test_sort_zone_and_facade(test_case):
    # test_case = read_existing_idf(path_class.models / TEST_CASE)
    zones = get_zones(test_case.idf)
    z = Zone(zones[0])
    drn = WallNormal.NORTH

    # NOTE: False = 0, so comes first in sorted list 
    res = sort_zone_and_facade_list([drn, z])
    assert list(res) == [z, drn]


NodeNames = Literal["WEST", "EAST", "NORTH", "SOUTH", "a", "b", "c"]


class PathCoordPair(NamedTuple):
    nodes: list[NodeNames]
    coords: list[tuple]


# TODO should have perimeter info no?
# skipping midpoints
test_wc = PathCoordPair(["WEST", "c"], [(0, 2), (1, 2.5), (2, 2.5)])
test_ecw = PathCoordPair(["WEST", "c", "EAST"], test_wc.coords + [(3, 2.5), (4, 2)])
test_sb = PathCoordPair(["SOUTH", "b"], [(2, 0), (1.5, 1), (1.5, 1.5)])
test_sbcn = PathCoordPair(
    ["SOUTH", "b", "c", "NORTH"], test_sb.coords + [(1.5, 2), (2, 2.5), (2, 3), (2, 4)]
)
test_bc = PathCoordPair(["b", "c"], [(1.5, 1.5), (1.5, 2), (2, 2.5)])


tests = [test_wc, test_ecw, test_sb, test_sbcn, test_bc]


# @pytest.mark.skip("Not implemented")
@pytest.mark.parametrize("pair", tests)
def test_connectivity_coords(pair, test_case):
    # test_case = read_existing_idf(path_class.models / TEST_CASE)
    coords = find_points_along_path(test_case.idf, pair.nodes)
    simple_coords = [i.pair for i in coords]
    assert simple_coords == pair.coords


if __name__ == "__main__":
    pass
    # test_connectivity_coords(test_sbcn)
    # test_sort_zone_and_facade()

    # test_connectivity_coords(test_ew)


# more so plotting..
# def test_create_plan_zones():
#     case = EneryPlusCaseEditor(path_to_outputs=path_class.models / FOLDER)
#     case.idf = add_rooms(case.idf, path_to_inputs=path_class.plans / FOLDER)
#     pz = PlanZones(case.idf)
#     p = pz.plot_zone_domains() # TODO plot w/ external positions?
