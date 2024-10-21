from copy import deepcopy
from eppy.bunch_subclass import EpBunch
from geomeppy import IDF

from subsurfaces.interfaces import Dimensions
from helpers.ep_helpers import create_domain_for_rectangular_wall
from subsurfaces.interfaces import SubsurfacePair, SubsurfaceObjects
from helpers.ep_helpers import WallNormal
from helpers.ep_helpers import get_zone_walls, get_zone_name
from subsurfaces.placement import create_nine_points_for_domain


class MoreThanOneIntersectionError(Exception):
    def __init__(self, surfaces: list[EpBunch]) -> None:
        super().__init__(surfaces)
        self.surfaces = surfaces


def handle_connection_result(res: list[EpBunch]):
    if len(res) == 0:
        raise Exception("No intersection")
    if len(res) == 1:
        return res[0]
    if len(res) > 1:
        raise MoreThanOneIntersectionError(res)


def find_surface_connecting_two_zones(idf: IDF, pair: SubsurfacePair):
    assert pair.space_b + 1  # type: ignore

    zone_walls = get_zone_walls(idf, pair.space_a)
    partner = get_zone_name(pair.space_b)  # type: ignore
    return handle_connection_result(
        [i for i in zone_walls if partner in i.Outside_Boundary_Condition_Object]
    )


def find_surface_connecting_zone_and_drn(idf: IDF, pair: SubsurfacePair):
    assert pair.space_b.name  # type: ignore
    zone_walls = get_zone_walls(idf, pair.space_a)
    try:
        res = handle_connection_result(
            [i for i in zone_walls if WallNormal(i.azimuth) == pair.space_b]
        )
        return res
    except MoreThanOneIntersectionError as err:
        # can put more complex logic here..
        return err.surfaces[0]


def get_connecting_surface(idf: IDF, pair: SubsurfacePair):
    if pair.attrs.object_type == SubsurfaceObjects.WINDOW:
        return find_surface_connecting_zone_and_drn(idf, pair)
    else:
        return find_surface_connecting_two_zones(idf, pair)


def is_dim_greater(subsurf_val, surf_val, dim):
    check = surf_val > subsurf_val
    if not check:
        # TODO: Log this ..
        # print(f"{dim}: {surf_val:.2f} NOT GREATER THAN {subsurf_val}")
        return False
    return True


def ensure_subsurface_within_surface(
    surf: EpBunch, pair: SubsurfacePair, correction: float = 0.9
):
    attrs = deepcopy(pair.attrs)
    subsurf_width = attrs.dimensions.width
    subsurf_height = attrs.dimensions.height
    try:
        assert is_dim_greater(subsurf_width, surf.width, "width")
        assert is_dim_greater(subsurf_height, surf.height, "height")
    except:
        # TODO should only edit 1
        # print(f"Editing {pair.space_a, pair.space_b} \n")
        attrs.dimensions.width = correction * float(surf.width)
        attrs.dimensions.height = correction * float(surf.height)
    return attrs


def get_approp_surface_and_attrs(
    idf: IDF,
    pair: SubsurfacePair,
):
    surf = get_connecting_surface(idf, pair)
    if not surf:
        raise Exception("No surface found")
    pair.attrs = ensure_subsurface_within_surface(surf, pair)
    return surf, pair.attrs


def create_starting_coord(surface: EpBunch, dim: Dimensions, loc: str):
    domain = create_domain_for_rectangular_wall(surface)
    np_dict = create_nine_points_for_domain(domain)

    assert loc in np_dict.keys()
    placement_details = np_dict[loc]

    coord = placement_details.point
    for fx in placement_details.functions:
        coord = fx(coord, dim)
    return coord
