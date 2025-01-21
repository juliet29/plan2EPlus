from geomeppy import IDF
from helpers.helpers import set_difference, list_all_dict_values
from helpers.ep_helpers import create_zone_map_without_partners


def get_afn_zones_and_subsurfaces(idf: IDF):
    # TODO make this more expressive, so know from function name it is mapping subsurfaces to zones.. 
    zone_map = create_zone_map_without_partners(idf)
    filtered_zone_map = {k: v for k, v in zone_map.items() if len(v) < 2}
    afn_zones = set_difference(zone_map.keys(), filtered_zone_map.keys())
    afn_subsurfaces = set_difference(
        list_all_dict_values(zone_map), list_all_dict_values(filtered_zone_map)
    )
    return afn_zones, afn_subsurfaces
