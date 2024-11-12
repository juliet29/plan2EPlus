from itertools import groupby
from geomeppy import IDF
from eppy.bunch_subclass import EpBunch

from helpers.ep_helpers import WallNormal, get_zone_walls, get_zones
from helpers.geometry_interfaces import Coordinate3D, Domain, Range


def create_total_range(res: list[Domain]):
    mins = [i.width.min for i in res]
    maxes = [i.width.max for i in res]
    return Range(min(mins), max(maxes))


def get_coords(surface):  # TODO move to ep_geom_helpers
    coords = [Coordinate3D(*i) for i in surface.coords]  # type:ignore
    assert len(coords) == 4
    xs = sorted(set([i.x for i in coords]))
    ys = sorted(set([i.y for i in coords]))
    zs = sorted(set([i.z for i in coords]))
    return xs, ys, zs


def create_domain_for_rectangular_wall(surface: EpBunch):
    xs, ys, zs = get_coords(surface)
    width = Range(*ys) if len(ys) > 1 else Range(*xs)
    height = Range(*zs)
    return Domain(width, height)


def create_domain_for_subsurface(subsurface: EpBunch):
    x0 = float(subsurface.Starting_X_Coordinate)
    y0 = float(subsurface.Starting_Z_Coordinate)
    x1 = x0 + float(subsurface.Length)
    y1 = y0 + float(subsurface.Height)
    return Domain(Range(x0, x1), Range(y0, y1))


def create_domain_for_zone(idf: IDF, num: int):
    def sort_and_group_walls():
        wall_pairs = [(WallNormal(round(float(i.azimuth))).name, i) for i in walls]
        sorted_objs = sorted(wall_pairs, key=lambda x: x[0])
        grouped_walls = {}
        for k, g in groupby(sorted_objs, key=lambda x: x[0]):
            grouped_walls[k] = list([i[1] for i in g])
        return grouped_walls

    def create_domains():
        domains = {}
        for k, v in grouped_walls.items():
            domains[k] = []
            for surf in v:
                domains[k].append(create_domain_for_rectangular_wall(surf))
        return domains

    walls = get_zone_walls(idf, num)
    grouped_walls = sort_and_group_walls()
    domains = create_domains()
    ranges = {k: create_total_range(v) for k, v in domains.items()}

    assert ranges["EAST"] == ranges["WEST"]
    assert ranges["NORTH"] == ranges["SOUTH"]
    return Domain(ranges["NORTH"], ranges["EAST"])


def get_zone_domains(idf: IDF):
    z = get_zones(idf)
    return [create_domain_for_zone(idf, ix) for ix, _ in enumerate(z)]

