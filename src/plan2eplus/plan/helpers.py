from pathlib import Path
from typing import Optional

from plan2eplus.helpers.helpers import load_data_from_json
from .interfaces import RoomFromJSON, PLAN


def get_plans_from_file(path_to_input: Path, plan_name: Optional[str] = PLAN):
    if not plan_name:
        plan_name = PLAN
    plan_data = load_data_from_json(path_to_input, plan_name)
    # print(plan_data)

    return [RoomFromJSON(**i) for i in plan_data[0]]  # TODO remove the double list..


def create_room_map(path_to_input: Path, plan_name=None) -> dict[int, str]:
    plan_data = get_plans_from_file(path_to_input, plan_name)
    room_map: dict[int, str] = {}
    for item in plan_data:
        room_map[item.id] = item.label
    return room_map
