from pathlib import Path
from plan.interfaces import RoomFromJSON
from geomeppy import IDF
from copy import deepcopy
from plan.helpers import get_plans_from_file


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


def add_eppy_blocks_to_case(_idf: IDF, path_to_input: Path):
    idf = deepcopy(_idf)
    height = get_room_height()
    plan = get_plans_from_file(path_to_input)
    for room in plan:
        block = convert_room_to_eppy_block(room, height)
        idf.add_block(**block)

    return idf
