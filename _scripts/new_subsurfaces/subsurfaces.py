from typing import NamedTuple
from new_subsurfaces.interfaces import SubsurfacePair, SubsurfaceType
from geomeppy.patches import EpBunch
from geomeppy import IDF
from geometry.wall_normal import WallNormal

# helpers





def idf_zone_to_surfaces(idf_zone: EpBunch):
    pass


# BUILDINGSURFACE
# ZONE f"


def get_zone_name(num: int):
    return f"Block 0{num} Storey 0"


def get_zone_surfaces(idf: IDF, num: int):
    return [
        i
        for i in idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        if get_zone_name(num) in i.Name
    ]


def get_zones(idf: IDF):
    return [i for i in idf.idfobjects["ZONE"]]


# class BuildingSurface_Detailed:
#     Name: str
#     Surface_Type: str


# ----------

class MoreThanOneIntersectionError(Exception):
    def __init__(self, surfaces: list[EpBunch]) -> None:
        super().__init__(surfaces)
        self.surfaces = surfaces


def handle_res(res: list[EpBunch]):
    if len(res) == 0:
        raise Exception("No intersection")
    if len(res) == 1:
        return res[0]
    if len(res) > 1:
        raise MoreThanOneIntersectionError(res)

def find_surface_connecting_two_zones(idf: IDF, pair: SubsurfacePair):
    assert pair.space_b + 1  # type: ignore

    zone_surfaces = get_zone_surfaces(idf, pair.space_a)
    partner = get_zone_name(pair.space_b) # type: ignore
    return handle_res(
        [i for i in zone_surfaces if partner in i.Outside_Boundary_Condition_Object]
    )


def find_surface_connecting_zone_and_drn(idf: IDF, pair: SubsurfacePair):
    assert pair.space_b.name # type: ignore
    zone_surfaces = get_zone_surfaces(idf, pair.space_a)
    try:
        res = handle_res(
            [i for i in zone_surfaces if WallNormal(i.azimuth) == pair.space_b]
        )
        return res
    except MoreThanOneIntersectionError as err:
        # TODO can put more complex logic here.. 
        return err.surfaces[0]


def get_connecting_surface(idf: IDF, pair: SubsurfacePair):
    if pair.attrs.object_type == SubsurfaceType.WINDOW:
        return find_surface_connecting_zone_and_drn(idf, pair)
    else:
        return find_surface_connecting_two_zones(idf, pair)
