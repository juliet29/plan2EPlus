import json
from plan.interfaces import PlanAccess, PLAN
from plan.room_to_eppy import RoomtoEppyBlock
from geomeppy import IDF
from copy import deepcopy

def get_plans_from_file(access: PlanAccess):
    with open(access.path / PLAN) as f:
        plan_data = json.load(f)
    return plan_data[access.index]

def get_room_height():
    # TODO rn fix room height 
    return 3.05 # m ~ 10ft 

def create_eppy_blocks(access: PlanAccess):
    plan = get_plans_from_file(access)
    blocks = []
    for room in plan:
        g = RoomtoEppyBlock(room, room_height=get_room_height())
        blocks.append(g.eppy_block)
    return blocks


def add_eppy_blocks_to_case(_idf:IDF, access:PlanAccess):
    idf = deepcopy(_idf)
    blocks = create_eppy_blocks(access)
    for block in blocks:
        idf.add_block(**block)

    return idf
