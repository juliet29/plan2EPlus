from dataclasses import dataclass
from geomeppy import IDF

# from plan2eplus.helpers.helpers import pairwise
from plan2eplus.visuals.interfaces import PlanZones, Surface, Zone
from rich import print as rprint
import logging
from plan2eplus.custom_exceptions import PlanMismatchException
from plan2eplus.geometry.directions import WallNormal
from typing import NamedTuple, Optional
from plan2eplus.geometry.coords import PerimeterMidpoints
from utils4plans.lists import (
    pairwise,
    chain_flatten,
    get_unique_items_in_list_keep_order,
)

from plan2eplus.geometry.coords import Coord

logger = logging.getLogger(__name__)

# TODO this somewhat duplicates existing surface logic.. -> can maybe go somewhere more general..


def find_wall_connecting_zones(idf: IDF, z0: Zone, z1: Zone) -> Surface:
    # now, do these zones share a wall..
    shared_walls = []
    for wall in z0.interior_walls:
        partner_wall = wall.partner_wall(idf)
        if partner_wall:
            # rprint(f"partner wall for {wall} is {partner_wall}")
            if partner_wall in z1.interior_walls:
                shared_walls.append(wall)
            else:
                logger.debug(
                    f"partner wall for {wall} not found in interior walls of {z1} -> {z1.interior_walls}"
                )
        else:
            logger.debug(f"No partner wall for {wall}")
    assert len(shared_walls) == 1, (
        "There should only be one wall that is shared by two zones"
    )
    return shared_walls[0]


def is_Zone(item):
    return hasattr(item, "directed_walls")


def sort_zone_and_facade_list(
    values: list[Zone | WallNormal],
) -> tuple[Zone, WallNormal]:
    assert len(values) == 2
    return tuple(sorted(values, key=lambda x: not is_Zone(x)))  # type: ignore


def find_directed_wall_of_zone(zone: Zone, drn: WallNormal) -> Surface:
    res = zone.directed_walls[drn.name]
    assert len(res) == 1, (
        f"There should only be one wall on the {drn.value} facade since it is an outer facade!"
    )
    return res[0]


# TODO: the file should actually start here..
class CoordTriplet(NamedTuple):
    first: Coord
    second: Coord
    third: Coord


def collapse_coord_triplets(lst: list[CoordTriplet]):
    flat_list = chain_flatten([list(i) for i in lst])
    return get_unique_items_in_list_keep_order(flat_list)


def get_drn_coord(pz: PlanZones, item: WallNormal):
    return pz.domains.external_coord_positions[item.name]


def get_zone_coord(zone: Zone):
    return zone.domain.centroid


def get_wall_coord(wall: Surface):
    return wall.centroid


def find_points_along_path(idf: IDF, path: list[str]):
    def get_space(item: str):
        try:
            return pz.get_zone_by_plan_name(item)
        except PlanMismatchException:
            return WallNormal[item]

    def get_coords(a, b):
        are_both_zones = all([is_Zone(i) for i in [a, b]])
        if are_both_zones:
            coords = [get_zone_coord(i) for i in [a, b]]
            shared_wall = get_wall_coord(find_wall_connecting_zones(idf, a, b))
            return CoordTriplet(coords[0], shared_wall, coords[1])
        else:
            # one direction, one zone.
            zone, drn = sort_zone_and_facade_list([a, b])
            zone_coord = get_zone_coord(zone)
            drn_coord = get_drn_coord(pz, drn)

            shared_wall = get_wall_coord(find_directed_wall_of_zone(zone, drn))
            if [zone, drn] == [a, b]:
                return CoordTriplet(zone_coord, shared_wall, drn_coord)
            else:
                return CoordTriplet(drn_coord, shared_wall, zone_coord)

    pz = PlanZones(idf)
    spaces = [get_space(i) for i in path]
    triplets = [get_coords(a, b) for a, b in pairwise(spaces)]
    return collapse_coord_triplets(triplets)
