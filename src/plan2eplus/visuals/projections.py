from typing import Literal
from eppy.bunch_subclass import EpBunch
from eppy.geometry.surface import get_an_unit_normal, unit_normal
from geomeppy.geom.polygons import Polygon, Polygon3D
from rich import print as rprint

from plan2eplus.helpers.ep_geom_helpers import Coordinate3D
from plan2eplus.helpers.geometry_interfaces import Domain

UNIT_NORMAL_DRN = Literal["X", "Y", "Z"]


def compute_unit_normal(surface: EpBunch) -> UNIT_NORMAL_DRN:
    vector_map: dict[tuple[int, int, int], UNIT_NORMAL_DRN] = {
        (1, 0, 0): "X",
        (0, 1, 0): "Y",
        (0, 0, 1): "Z",
    }
    normal_vector = Polygon3D(surface.coords).normal_vector
    nv = tuple([abs(int(i)) for i in normal_vector])
    assert len(nv) == 3
    return vector_map[nv]


def get_surface_coords(surface: EpBunch):
    surf_coords = surface.coords
    assert surf_coords
    return [Coordinate3D(*i) for i in surf_coords]


def get_position_along_normal_axis(surface: EpBunch, unit_normal_drn: UNIT_NORMAL_DRN):
    coords = get_surface_coords(surface)
    if unit_normal_drn == "X":
        val = [i.x for i in coords]
    elif unit_normal_drn == "Y":
        val = [i.y for i in coords]
    else:
        raise NotImplementedError("only considered x + y!")
    assert len(set(val)) == 1, f"{val} should all have the same numbers!"
    return val[0]


def get_surface_domain(surface: EpBunch, unit_normal_drn: UNIT_NORMAL_DRN):
    match unit_normal_drn:
        case "X":
            pair = ("y", "z")
        case "Y":
            pair = ("x", "z")
        case "Z":
            pair = ("x", "y")
        case _:
            raise Exception("Invalid Direction!")

    def get_coords(l1, l2):
        return [coord.get_pair(l1, l2) for coord in coords]

    coords = get_surface_coords(surface)
    coords_2D = get_coords(*pair)
    return Domain.from_coords_list(coords_2D)
