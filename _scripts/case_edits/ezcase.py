from dataclasses import dataclass
from typing import List, Tuple, Union
from outputs.variables import OutputVars 
from case_edits.epcase import EneryPlusCaseEditor

from gplan.room_type import GPLANRoomType, GPLANRoomAccess
from gplan.convert import GPLANtoGeomeppy
# from case_edits.methods.subsurfaces.surface_getter import SurfaceGetter



@dataclass
class EzCaseInput:
    case_name:str
    door_pairs:List[Tuple]

    geometry:Union[List[GPLANRoomType], GPLANRoomAccess] = GPLANRoomAccess("",0)
    starting_case:str=""
    
    # window_pairs:List[Tuple]
    # outputs:List[OutputVars]

class EzCase():
    def __init__(self, input:EzCaseInput) -> None:
        self.case_name = input.case_name
        self.geometry = input.geometry
        self.door_pairs = input.door_pairs
        self.starting_case = input.starting_case

        self.case = EneryPlusCaseEditor(self.case_name, self.starting_case)

        self.run()

    def run(self):
        self.add_rooms()
        self.get_geometry()

    def add_rooms(self):
        self.gplan_convert = GPLANtoGeomeppy(self.case, self.geometry)
        self.case.idf.intersect_match()
        self.case.idf.set_default_constructions()

    def get_geometry(self):
        self.case.get_geometry()
        self.zones = self.case.geometry.zones

    # def get_surface(self):
    #     # TODO will be part of doors.. just testing 
    #     self.sg = SurfaceGetter(self)

