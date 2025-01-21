from copy import deepcopy
from pathlib import Path

from geomeppy import IDF
from .helpers import get_plans_from_file
from .interfaces import RoomFromJSON
from ..case_edits.extended_idf import ExtendedIDF


def get_room_height():
    # rn fix room height
    return 3.05  # m ~ 10ft


def convert_room_to_eppy_block(room: RoomFromJSON, height: float):
    domain = room.create_domain()
    return {
        "name": room.create_zone_name(),
        "coordinates": domain.create_coordinates(),
        "height": height,
    }


def add_eppy_blocks(_idf: ExtendedIDF, plan: list[RoomFromJSON]):
    idf = deepcopy(_idf)
    for room in plan:
        block = convert_room_to_eppy_block(room, _idf.modifications.height)
        idf.add_block(**block)

    return idf


def add_eppy_blocks_from_file(_idf: IDF, path_to_input: Path):
    plan = get_plans_from_file(path_to_input)
    return add_eppy_blocks(_idf, plan)
