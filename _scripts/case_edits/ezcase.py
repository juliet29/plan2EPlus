from dataclasses import dataclass
from typing import List, Tuple, Union
from outputs.variables import OutputVars 
from case_edits.epcase import EneryPlusCaseEditor

from gplan.room_type import GPLANRoomType, GPLANRoomAccess
from gplan.convert import GPLANtoGeomeppy



@dataclass
class EzCaseStarter:
    case_name:str

    geometry:Union[List[GPLANRoomType], GPLANRoomAccess] = GPLANRoomAccess("",0)# TODO check / create custom type for GPLAN things 
    starting_case:str=""

    # door_pairs:List[Tuple]
    # window_pairs:List[Tuple]
    # outputs:List[OutputVars]

# defstart = EzCaseStarter(case_name="TEST_CASE", geometry=GPLANRoomAccess("", 0))

class EzCase(EzCaseStarter):
    def __init__(self, starter:EzCaseStarter) -> None:
        self.case_name = starter.case_name
        self.geometry = starter.geometry
        
        # print(self.case_name)

        self.case = EneryPlusCaseEditor(self.case_name, self.starting_case)

    def add_rooms(self):
        self.gplan_convert = GPLANtoGeomeppy(self.case, self.geometry)
        # self.case.idf.intersect_match()
        self.case.idf.set_default_constructions()
