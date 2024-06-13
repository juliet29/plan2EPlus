from icecream import ic
from geomeppy import IDF

from case_edits.epcase import EneryPlusCaseEditor
from geometry.wall import Wall

DOOR_GAP = 2/100 #m 

class DoorAttributes:
    def __init__(self, length, height) -> None:
        self.length = length 
        self.height = height
        self.half_length = self.length/2
        



class Door:
    def __init__(self, epcase:EneryPlusCaseEditor, door_attrs:DoorAttributes) -> None:
        self.epcase = epcase
        self.attrs = door_attrs


    def set_surface(self, surface):
        # TODO select from epcase idf using epbunch
        self.surface = surface

    def set_construction(self, constr_name):
        self.construction = constr_name

    # TODO check attrs width and height less than wall width and height

    def create_door(self):
        self.create_door_name()
        self.calculate_door_start_coords()
        self.create_door_object()

    def create_door_name(self):
        self.name = f"{self.surface.Name} Door"
        # TODO check that no object with this name 

    def calculate_door_start_coords(self):
        center_width = self.surface.width/2

        self.start_x = center_width - self.attrs.half_length
        self.start_z = DOOR_GAP

    def create_door_object(self):
        self.epcase.idf.newidfobject("DOOR")
        door_obj = self.epcase.idf.idfobjects["DOOR"][-1]

        door_obj.Starting_X_Coordinate = self.start_x
        door_obj.Starting_Z_Coordinate = self.start_z
        door_obj.Height = self.attrs.height
        door_obj.Length = self.attrs.length
        door_obj.Construction_Name = self.construction
        door_obj.Building_Surface_Name = self.surface.Name
        door_obj.Name = self.name

    # TODO be able to visualize doors in geometry .. 

        
        
    