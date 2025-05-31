from typing import NamedTuple
from rich import print as rprint

from plan2eplus.helpers.helpers import regex_match


class ConstructionTypeMap(NamedTuple):
    default_name: str
    possible_names: list[str]


default_maps = [
    ConstructionTypeMap("exterior", ["exterior"]),
    ConstructionTypeMap("interior", ["interior", "partition"]),
    ConstructionTypeMap("roof", ["roof"]),
    ConstructionTypeMap("cieling", ["cieling"]), # treat as edge case if unassigned.. 
    ConstructionTypeMap("floor", ["floor"]),
    ConstructionTypeMap("door", ["door"]),
    ConstructionTypeMap("window", ["window"]),
]


given_names = ["My Exterior Wall", "My Partitions", "My Roof/Ceiling", "My Floor"]

## if any of the possible names is in the construction name, then it gets assigned the default name.. 

def match_construction_to_default(given, possible_names:list[str]):
    for possible in possible_names:
        pattern_str = fr"{possible}"
        res = regex_match(pattern_str, given, IGNORE_CASE=True)
        if res:
            # rprint(res)
            return True
        
def find_construction_name_in_defualts(given_name: str, map=default_maps):
    for map in default_maps:
        res = match_construction_to_default(given_name, map.possible_names)
        if res:
            rprint(f"{given} matches with {map.default_name}")
            return True
    rprint(f"{given} DID NOT MATCH!")
        

    

if __name__ == "__main__":
    given = "My_Exterior_wall"
    possible = "exterior"
    # match_construction_to_default(given, possible)
    for given in given_names:
        find_construction_name_in_defualts(given)
        # realistically some flag here.. but doing this on the object level..     
        
# TODO assign idf surfaces based on the construction that alignes with them.. 
