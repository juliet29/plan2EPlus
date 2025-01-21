from plan2eplus.config import IDD_PATH, IDF_PATH
from plan2eplus.case_edits.extended_idf import ExtendedIDF
from plan2eplus.plan.local_room_def import RoomDefinition, create_two_room_layout
from plan2eplus.plan.plan_to_eppy import add_eppy_blocks

def run_ezcase():
    ExtendedIDF.setiddname(IDD_PATH)
    idf1 = ExtendedIDF(IDF_PATH)

    plan = create_two_room_layout(RoomDefinition(5, 5), RoomDefinition(10, 5))
    idf1 = add_eppy_blocks(idf1, plan)
    return idf1