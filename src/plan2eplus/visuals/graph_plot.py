from geomeppy import IDF

# from plan2eplus.helpers.helpers import pairwise
from plan2eplus.visuals.interfaces import PlanZones, Surface, Zone
from rich import print as rprint
import logging
from plan2eplus.custom_exceptions import PlanMismatch
from plan2eplus.helpers.geometry_interfaces import WallNormal
from itertools import pairwise
from typing import NamedTuple


logger = logging.getLogger(__name__)


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
    assert len(shared_walls) == 1,  "There should only be one wall that is shared by two zones"
    return shared_walls[0]


def find_wall_on_zone_facade(idf: IDF, zone: Zone, drn: WallNormal) -> Surface:
    res = zone.directed_walls[drn.name]
    assert len(res) == 1, f"There should only be one wall on {drn.value} facade"

    return res[0]


class ZoneDrnPair(NamedTuple):
    zone: Zone
    drn: WallNormal


def find_points_along_path(idf: IDF):
    pz = PlanZones(idf)
    pz.plot_zone_domains()
    # path = ["NORTH", "c", "a", "SOUTH"]
    path = ["WEST", "b", "a", "EAST"]

    spaces: list[Zone | WallNormal] = []

    for space in path:
        try:
            spaces.append(pz.get_zone_by_plan_name(space))
        except PlanMismatch:
            spaces.append(WallNormal[space])

    shared_walls: list[Surface] = []
    # rprint(spaces)
    for a, b in pairwise(spaces):
        # rprint((a,b))
        if isinstance(a, Zone) and isinstance(b, Zone):
            shared_wall = find_wall_connecting_zones(idf, a, b)
        else:
            res = sorted([a, b], key=lambda x: isinstance(x, WallNormal))
            shared_wall = find_wall_on_zone_facade(idf, *ZoneDrnPair(*res)) # type: ignore -> typechecker does not know about sorting results 
        # rprint([a, b, shared_wall])
        shared_walls.append(shared_wall)

    rprint([(i, i.centroid) for  i in shared_walls])
    # TODO append the centroid of the zone  / positoon f the endpoints..
