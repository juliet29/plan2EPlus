from dataclasses import dataclass
from typing import List, Tuple, Union
from outputs.variables import OutputVars 
from case_edits.epcase import EneryPlusCaseEditor

from gplan.room_type import GPLANRoomType, GPLANRoomAccess
from gplan.convert import GPLANtoGeomeppy


from case_edits.methods.subsurfaces.inputs import SubsurfaceInputs, SubsurfaceAttributes, SubsurfaceType
from case_edits.methods.subsurfaces.subsurface import Subsurface




@dataclass
class EzCaseInput:
    case_name:str
    door_pairs:List[Tuple]
    window_pairs:List[Tuple]

    geometry:Union[List[GPLANRoomType], GPLANRoomAccess] = GPLANRoomAccess("",0)
    starting_case:str=""
    
   
    # outputs:List[OutputVars]

class EzCase():
    def __init__(self, input:EzCaseInput) -> None:
        self.input = input

        self.case = EneryPlusCaseEditor(self.input.case_name, self.input.starting_case)

        self.run()

    def run(self):
        self.add_rooms()
        self.get_subsurface_constructions()
        self.get_geometry()

    def add_rooms(self):
        self.gplan_convert = GPLANtoGeomeppy(self.case, self.input.geometry)
        self.case.idf.intersect_match()
        self.case.idf.set_default_constructions()
        
        
    def get_geometry(self):
        self.case.get_geometry()
        self.zones = self.case.geometry.zones

    def get_subsurface_constructions(self):
        self.door_const = self.case.idf.getobject("CONSTRUCTION", "Project Door")
        self.window_const = self.case.idf.getobject("CONSTRUCTION", "Project External Window")


    def add_doors(self):
        standard_door = SubsurfaceAttributes(SubsurfaceType.DOOR, 1, 2, self.door_const) #type:ignore
        inputs = SubsurfaceInputs(self.zones, self.input.door_pairs, self.case.idf, standard_door)
        self.ss = Subsurface(inputs)
        self.ss.create_all_ssurface()

    def add_windows(self):
        standard_window = SubsurfaceAttributes(SubsurfaceType.WINDOW, 0.5, 0.5, self.window_const) #type:ignore
        inputs = SubsurfaceInputs(self.zones, self.input.window_pairs, self.case.idf, standard_window)
        self.ss = Subsurface(inputs)
        self.ss.create_all_ssurface()


