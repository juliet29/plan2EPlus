from geomeppy import IDF
from eppy.bunch_subclass import EpBunch

from helpers.geometry_interfaces import Coordinate3D, Domain, Range

from enum import Enum


class WallNormal(Enum):
    # direction of outward normal of the wall..
    # https://eppy.readthedocs.io/en/latest/eppy.geometry.html#eppy.geometry.surface.azimuth
    NORTH = 0.0
    EAST = 90.0
    SOUTH = 180.0
    WEST = 270.0

    def __getitem__(self, i):
        return getattr(self, i)


def get_zone_name(num: int):
    return f"Block 0{num} Storey 0"


def get_zones(idf: IDF) -> list[EpBunch]:
    return [i for i in idf.idfobjects["ZONE"]]


def get_zone_walls(idf: IDF, num: int) -> list[EpBunch]:
    return [
        i
        for i in idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        if get_zone_name(num) in i.Name and "Wall" in i.Name
    ]



def is_interior_wall(surf: EpBunch):
    return surf.Surface_Type == "wall" and surf.Outside_Boundary_Condition == "surface"

def get_surface_of_subsurface(idf:IDF, subsurface: EpBunch):
    return idf.getobject("BUILDINGSURFACE:DETAILED", subsurface.Building_Surface_Name)

def get_subsurface_by_name(idf: IDF, name: str):
    subsurfaces = idf.getsubsurfaces()
    return [i for i in subsurfaces if name == i.Name][0]


PARTNER = " Partner"
def create_partner_name(name: str):
    return name + PARTNER
def reverse_partner_name(partner_name: str):
    return partner_name.replace(PARTNER, "")

def find_zone_subsurfaces(zone_name: str, subsurfaces: list[EpBunch]) -> list[str]:
    return [s.Name for s in subsurfaces if zone_name in s.Building_Surface_Name]

def create_zone_map(idf:IDF) -> dict[str, list[str]]:
    zones = get_zones(idf)
    subsurfaces = idf.getsubsurfaces()
    return {z.Name: find_zone_subsurfaces(z.Name, subsurfaces) for z in zones}

# TODO use for AFN.. 
def create_zone_map_without_partners(idf:IDF):
    zone_map = create_zone_map(idf)
    for k, v in zone_map.items():
        for ix, name in enumerate(v):
            if PARTNER in name:
                zone_map[k][ix] = reverse_partner_name(name)
    return zone_map






## geometry... 

def create_domain_for_rectangular_wall(surface: EpBunch):
    coords = [Coordinate3D(*i) for i in surface.coords]  # type:ignore
    assert len(coords) == 4
    xs = sorted(set([i.x for i in coords]))
    ys = sorted(set([i.y for i in coords]))
    zs = sorted(set([i.z for i in coords]))

    width = Range(*ys) if len(ys) > 1 else Range(*xs)
    height = Range(*zs)
    return Domain(width, height)


def create_domain_for_subsurface(subsurface: EpBunch):
    x0 = float(subsurface.Starting_X_Coordinate)
    y0 = float(subsurface.Starting_Z_Coordinate)
    x1 = x0 + float(subsurface.Length)
    y1 = y0 + float(subsurface.Height)
    return Domain(Range(x0, x1), Range(y0, y1))
    
