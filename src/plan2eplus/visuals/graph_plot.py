from geomeppy import IDF
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

# from plan2eplus.helpers.helpers import pairwise
from plan2eplus.visuals.interfaces import PlanZones, Surface, Zone
from rich import print as rprint
import logging
from plan2eplus.custom_exceptions import PlanMismatch
from plan2eplus.helpers.geometry_interfaces import WallNormal
from itertools import pairwise
from typing import NamedTuple, Optional
from plan2eplus.helpers.geometry_interfaces import PerimeterMidpoints
from scipy.interpolate import CubicSpline
import numpy as np


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
    assert len(shared_walls) == 1, (
        "There should only be one wall that is shared by two zones"
    )
    return shared_walls[0]


def find_wall_on_zone_facade(idf: IDF, zone: Zone, drn: WallNormal) -> Surface:
    res = zone.directed_walls[drn.name]
    assert len(res) == 1, f"There should only be one wall on {drn.value} facade"

    return res[0]


class ZoneDrnPair(NamedTuple):
    zone: Zone
    drn: WallNormal


def find_points_along_path(idf: IDF, path: list[str]):
    pz = PlanZones(idf)
    assert path[0] in WallNormal.keys()
    assert path[-1] in WallNormal.keys()

    spaces: list[Zone | WallNormal] = []

    for space in path:
        try:
            spaces.append(pz.get_zone_by_plan_name(space))
        except PlanMismatch:
            spaces.append(WallNormal[space])

    shared_walls: list[Surface] = []

    for a, b in pairwise(spaces):
        if isinstance(a, Zone) and isinstance(
            b, Zone
        ):  # TODO why not a try-catch here also?
            shared_wall = find_wall_connecting_zones(idf, a, b)
        else:
            res = sorted([a, b], key=lambda x: isinstance(x, WallNormal))
            shared_wall = find_wall_on_zone_facade(idf, *ZoneDrnPair(*res))  # type: ignore -> typechecker does not know about sorting results # TODO find cleaner way to write this..
        shared_walls.append(shared_wall)

    # can reasonably assume that all paths will end and start with cardinal directions (for these lines..)
    coords = []
    start_coord = pz.domains.external_coord_positions[path[0]]
    end_coord = pz.domains.external_coord_positions[path[-1]]
    coords = [i.centroid for i in shared_walls]
    coords.insert(0, start_coord)
    coords.append(end_coord)

    # rprint([i for  i in shared_walls])
    # rprint(f"coords: {coords}")
    return coords
    # TODO append the centroid of the zone  / positoon f the endpoints..


def create_spline(xs, ys):
    cs = CubicSpline(xs, ys)
    line_xs = np.linspace(start=xs[0], stop=xs[-1], num=20)
    return line_xs, cs(line_xs)


def plot_path_on_plot(coords: list[tuple[float, float]], ax: Optional[Axes] = None):
    print(f"==>> coords: {coords}")
    if not ax:
        _, ax = plt.subplots()
    xs = [i[0] for i in coords]
    print(f"==>> xs: {xs}")
    ys = [i[1] for i in coords]
    print(f"==>> ys: {ys}")
    line_xs, line_ys = create_spline(xs, ys)
    ax.plot(line_xs, line_ys)
    return ax
