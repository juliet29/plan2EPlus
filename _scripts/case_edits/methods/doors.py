from icecream import ic
from geomeppy import IDF
from geomeppy.patches import EpBunch


from case_edits.epcase import EneryPlusCaseEditor
from geometry.wall import Wall

DOOR_GAP = 2/100 #m 

class DoorAttributes:
    def __init__(self, length, height) -> None:
        self.length = length 
        self.height = height
        self.half_length = self.length/2

default_door_attrs = DoorAttributes(1, 2)
        

class Door:
    def __init__(self, epcase:EneryPlusCaseEditor, door_attrs:DoorAttributes=default_door_attrs) -> None:
        self.epcase = epcase
        self.attrs = door_attrs


    def set_surface(self, surface:Wall):
        # TODO select from epcase idf using epbunch
        self.surface = surface

    def set_construction(self, constr:EpBunch):
        self.construction = constr

    # TODO check attrs width and height less than wall width and (height + DOOR_GAP)

    def create_door(self):
        assert self.surface and self.construction, "Surface and construction not added!"
        self.create_door_name()
        self.calculate_door_start_coords()
        self.initialize_door_object()
        self.update_door_attributes()
        if self.surface.is_interior_wall:
            self.make_partner_door_object()

    def create_door_name(self):
        self.name = f"{self.surface.name} Door"
        # TODO check that no other object with this name 

    def calculate_door_start_coords(self):
        center_width = int(self.surface.data.width)/2

        self.start_x = center_width - self.attrs.half_length
        self.start_z = DOOR_GAP


    def initialize_door_object(self):
        if self.surface.is_interior_wall:
            self.epcase.idf.newidfobject("DOOR:INTERZONE")
            self.door_obj = self.epcase.idf.idfobjects["DOOR:INTERZONE"][-1]
        else:
            self.epcase.idf.newidfobject("DOOR")
            self.door_obj = self.epcase.idf.idfobjects["DOOR"][-1]

    def update_door_attributes(self):
        self.door_obj.Starting_X_Coordinate = self.start_x
        self.door_obj.Starting_Z_Coordinate = self.start_z
        self.door_obj.Height = self.attrs.height
        self.door_obj.Length = self.attrs.length
        self.door_obj.Construction_Name = self.construction.Name
        self.door_obj.Building_Surface_Name = self.surface.name
        self.door_obj.Name = self.name

    def make_partner_door_object(self):
        self.epcase.idf.copyidfobject(self.door_obj)
        self.door2 = self.epcase.idf.idfobjects["DOOR:INTERZONE"][-1]
        self.door2.Name =  f"{self.surface.partner_wall_name} Door"
        self.door2.Building_Surface_Name = self.surface.partner_wall_name

        self.door2.Outside_Boundary_Condition_Object = self.door_obj.Name
        self.door_obj.Outside_Boundary_Condition_Object = self.door2.Name



    # TODO be able to visualize doors in geometry .. 

        
        
    