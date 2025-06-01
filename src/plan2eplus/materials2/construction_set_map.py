from typing import NamedTuple, Literal
from rich import print as rprint
from dataclasses import dataclass

from plan2eplus.helpers.helpers import regex_match
from plan2eplus.materials2.interfaces import (
    Construction,
    ConstructionTypes,
    create_test_constructions,
)
from plan2eplus.visuals.interfaces import Subsurface, Surface


class ConstructionTypeMap(NamedTuple):
    default_name: ConstructionTypes
    possible_names: list[str]


default_maps = [
    ConstructionTypeMap("exterior", ["exterior"]),
    ConstructionTypeMap("interior", ["interior", "partition"]),
    ConstructionTypeMap("roof", ["roof"]),
    ConstructionTypeMap("cieling", ["cieling"]),  # treat as edge case if unassigned..
    ConstructionTypeMap("floor", ["floor"]),
    ConstructionTypeMap("door", ["door"]),
    ConstructionTypeMap("window", ["window"]),
]
# TODO should be some heriarchy here..


given_names = ["My Exterior Wall", "My Partitions", "My Roof/Ceiling", "My Floor"]

## if any of the possible names is in the construction name, then it gets assigned the default name..


def match_construction_to_default(given, possible_names: list[str]):
    for possible in possible_names:
        pattern_str = rf"{possible}"
        res = regex_match(pattern_str, given, IGNORE_CASE=True)
        if res:
            # rprint(res)
            return True


def find_construction_name_in_defualts(construction: Construction, map=default_maps):
    # TODO make copy of the construction
    for map in default_maps:
        res = match_construction_to_default(construction.name, map.possible_names)
        if res:
            construction.assign_default_mapping(map.default_name)
            rprint(f"{construction.name} matches with {map.default_name}")
            return True
    rprint(f"{given} DID NOT MATCH!")


@dataclass
class ConstructionSet:
    exterior: Construction | None = None
    interior: Construction | None = None
    roof: Construction | None = None
    cieling: Construction | None = None
    floor: Construction | None = None
    door: Construction | None = None
    window: Construction | None = None

    def __setitem__(self, key, value):
        if key in [field for field in self.__annotations__.keys()]:
            setattr(self, key, value)
        else:
            raise KeyError(f"'{key}' is not a valid field for this dataclass")

    @classmethod
    def from_list_of_constructions(cls, constructions: list[Construction]):
        for const in constructions:
            find_construction_name_in_defualts(const)

        cset = cls()

        for const in constructions:
            if const.construction_type:
                cset[const.construction_type] = const
                # cls.__annotations__[const.construction_type] = const.name
        return cset
        # for k, v in cls.__annotations__.items():
        #     if not isinstance(v, str):
        #         cls.__annotations__[k] = None

        # return cls(**cls.__annotations__)


def match_surface_to_constr_set(surface: Surface | Subsurface, cset: ConstructionSet):

    # TODO make this deepcopy 
    if isinstance(surface, Surface):
        if surface.is_wall:
            if surface.is_interior:
                assert cset.interior
                surface.assign_construction(cset.interior.name)
            else:
                assert cset.exterior
                surface.assign_construction(cset.exterior.name)
        else:
            if surface.is_floor:
                assert cset.floor
                surface.assign_construction(cset.floor.name)
            if surface.is_roof:
                assert cset.roof
                surface.assign_construction(cset.roof.name)
    else:
        assert isinstance(surface, Subsurface)
        if surface.is_door:
            assert cset.door
            surface.assign_construction(cset.door.name)
        else:
            assert cset.window
            surface.assign_construction(cset.window.name)
    
    return surface


if __name__ == "__main__":
    given = "My_Exterior_wall"
    possible = "exterior"
    consts = create_test_constructions()

    # match_construction_to_default(given, possible)
    # for given in given_names:
    #     find_construction_name_in_defualts(given)
    for const in consts:
        find_construction_name_in_defualts(const)

    consset = ConstructionSet.from_list_of_constructions(list(consts))

    # realistically some flag here.. but doing this on the object level..

# TODO assign idf surfaces based on the construction that alignes with them..   1111111111111111                                111
