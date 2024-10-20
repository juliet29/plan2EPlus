from geomeppy import IDF
from eppy.bunch_subclass import EpBunch

from new_subsurfaces.geometry_interfaces import Coordinate3D, Domain, Range


def get_zone_name(num: int):
    return f"Block 0{num} Storey 0"


def get_zone_surfaces(idf: IDF, num: int) -> list[EpBunch]:
    return [
        i
        for i in idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        if get_zone_name(num) in i.Name
    ]


def get_zone_walls(idf: IDF, num: int) -> list[EpBunch]:
    return [
        i
        for i in idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        if get_zone_name(num) in i.Name and "Wall" in i.Name
    ]


def get_zones(idf: IDF) -> list[EpBunch]:
    return [i for i in idf.idfobjects["ZONE"]]


def is_interior_wall(surf: EpBunch):
    return surf.Surface_Type == "wall" and surf.Outside_Boundary_Condition == "surface"


def create_domain_for_rectangular_wall(surface: EpBunch):
    coords = [Coordinate3D(*i) for i in surface.coords]  # type:ignore
    assert len(coords) == 4
    xs = sorted(set([i.x for i in coords]))
    ys = sorted(set([i.y for i in coords]))
    zs = sorted(set([i.z for i in coords]))

    width = Range(*ys) if len(ys) > 1 else Range(*xs)
    height = Range(*zs)
    return Domain(width, height)
