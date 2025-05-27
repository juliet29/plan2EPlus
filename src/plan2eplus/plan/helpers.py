from pathlib import Path
import json
from typing import Optional
from .interfaces import RoomFromJSON, PLAN


def load_data_from_json(path_to_inputs, file_name):
    path = path_to_inputs / file_name
    assert path.exists(), f"{path} is not valid"
    with open(path) as f:
        res = json.load(f)
    return res


def get_plans_from_file(path_to_input: Path, plan_name:Optional[str]=PLAN):
    if not plan_name:
        plan_name = PLAN
    plan_data = load_data_from_json(path_to_input, plan_name)
    print(plan_data)

    return [RoomFromJSON(**i) for i in plan_data[0]]


def create_room_map(path_to_input: Path) -> dict[int, str]:
    plan_data = get_plans_from_file(path_to_input)
    room_map: dict[int, str] = {}
    for item in plan_data:
        room_map[item.id] = item.label
    return room_map

