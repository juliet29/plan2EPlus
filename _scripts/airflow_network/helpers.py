from geomeppy import IDF
from geomeppy.patches import EpBunch
from eppy.bunch_subclass import EpBunch as EPB

from helpers.ep_helpers import get_zones
# from helpers.helpers import *


def find_matching_zone(subsurface:EpBunch | EPB, zone_names: list[str]):
    for i in zone_names:
        if i in subsurface.Building_Surface_Name:
            return i
        
def pair_zone_and_subsurfaces(idf: IDF):
    zone_names = [i.Name for i in get_zones(idf)]
    original_subsurfaces = [i for i in idf.getsubsurfaces() if "Partner" not in i.Name]

    zone_pairs = [(find_matching_zone(i, zone_names), i.Name) for i in original_subsurfaces]

    d = {}
    for zone, subsurf in zone_pairs:
        if zone not in d.keys():
            d[zone] = []
        d[zone].append(subsurf)

    # remove zones w less than two subsurfaces
    return {k:v for k,v in d.items() if len(v) >= 2}
