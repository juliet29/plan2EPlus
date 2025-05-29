from dataclasses import dataclass
from ..helpers.geometry_interfaces import Dimensions
from ..helpers.geometry_interfaces import WallNormal
from .interfaces import RoomFromJSON


@dataclass
class RoomDefinition(Dimensions):
    label: str | None = ""


@dataclass
class EdgeDetails:
    source: int | str
    target: int | str
    direction: dict[str, WallNormal]


def initial_room(room_def: RoomDefinition):
    return RoomFromJSON(
        0, room_def.label, 0, 0, str(room_def.width), str(room_def.height)
    )


def adjacent_right(adj_room: RoomFromJSON, room_def: RoomDefinition):
    top = adj_room.top
    left = adj_room.create_domain().horz_range.max
    id = adj_room.id
    return RoomFromJSON(
        id, room_def.label, left, top, str(room_def.width), str(room_def.height)
    )


def create_two_room_layout(defn_a: RoomDefinition, defn_b: RoomDefinition):
    # TODO make extensible..
    rleft = initial_room(defn_a)
    rright = adjacent_right(rleft, defn_b)
    return [rleft, rright]
    # todo => should create graph as go along..
    # but what if just have input file?
    # can use shapely to get adjacencies in simple way..


# TODO if they are importing a json file, need to first check that the file is valid, and highlight places where it is not.. s
