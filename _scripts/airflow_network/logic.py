from geomeppy import IDF
from eppy.bunch_subclass import EpBunch

from helpers.helpers import chain_flatten
from helpers.ep_helpers import get_zones


def find_matching_zone(subsurface: EpBunch, zone_names: list[str]):
    for i in zone_names:
        if i in subsurface.Building_Surface_Name:
            return i
    raise Exception(f"Subsurface {subsurface.Name} does not have a matching zone!")


def pair_zone_and_subsurfaces(idf: IDF):
    zone_names = [i.Name for i in get_zones(idf)]
    original_subsurfaces = [i for i in idf.getsubsurfaces() if "Partner" not in i.Name]
    assert len(zone_names) > 0 and len(original_subsurfaces) > 0

    zone_pairs = [
        (find_matching_zone(i, zone_names), i.Name) for i in original_subsurfaces
    ]

    d: dict[str, list[str]] = {}
    for zone, subsurf in zone_pairs:
        if zone not in d.keys():
            d[zone] = []
        d[zone].append(subsurf)

    # remove zones w less than two subsurfaces
    d2 = {k: v for k, v in d.items() if len(v) >= 2}

    zones = set(d2.keys())
    subsurfaces = set(chain_flatten(d2.values()))

    return zones, subsurfaces
