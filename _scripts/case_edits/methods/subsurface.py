from icecream import ic
from typing import Union
from enum import Enum

from geomeppy import IDF
from geomeppy.patches import EpBunch



from case_edits.epcase import EneryPlusCaseEditor
from geometry.wall import Wall

DOOR_GAP = 2/100 #m 

class SubsurfaceType(Enum):
    DOOR = 0
    WINDOW = 1

class SubsurfaceAttributes:
    def __init__(self, type:SubsurfaceType, length:int, height:int, construction:EpBunch=None, surface:Wall=None) -> None: # type: ignore
        self.type = type
        self.length = length 
        self.height = height
        self.half_length = self.length/2
        self.construction = construction
        self.surface = surface
    
    def set_surface(self, surface:Wall):
        # TODO select from epcase idf using epbunch
        self.surface = surface

    def set_construction(self, constr:EpBunch):
        self.construction = constr
        

class Subsurface:
    def __init__(self, epcase:EneryPlusCaseEditor, attrs:SubsurfaceAttributes) -> None:
        self.epcase = epcase
        self.attrs = attrs

    # TODO check attrs width and height attrs.less than wall width and (height + DOOR_GAP)


    def create_surface(self):
        assert self.attrs.surface and self.attrs.construction, "Surface and construction not added!"

        self.determine_ssurface_type()
        self.create_ssurface_name()
        self.calculate_start_coords()
        self.initialize_object()
        self.update_attributes()
        if self.attrs.surface.is_interior_wall:
            self.make_partner_object()

    def determine_ssurface_type(self):
        self.type = self.attrs.type.name
        self.type_interzone = f"{self.type}:INTERZONE"
        self.type_title = self.type.title()

    def create_ssurface_name(self):
        self.name = f"{self.attrs.surface.name} {self.type_title}"
        # TODO check that no other object with this name 

    def calculate_start_coords(self):
        surface_center = int(self.attrs.surface.data.width)/2
        self.start_x = surface_center - self.attrs.half_length
        self.start_z = DOOR_GAP # TODO adjust for windeows  ! 


    def initialize_object(self):
        if self.attrs.surface.is_interior_wall:
            self.epcase.idf.newidfobject(self.type_interzone)
            self.obj0 = self.epcase.idf.idfobjects[self.type_interzone][-1]
        else:
            self.epcase.idf.newidfobject(self.type)
            self.obj0 = self.epcase.idf.idfobjects[self.type][-1]

    def update_attributes(self):
        self.obj0.Starting_X_Coordinate = self.start_x
        self.obj0.Starting_Z_Coordinate = self.start_z
        self.obj0.Height = self.attrs.height
        self.obj0.Length = self.attrs.length
        self.obj0.Construction_Name = self.attrs.construction.Name
        self.obj0.Building_Surface_Name = self.attrs.surface.name
        self.obj0.Name = self.name

    def make_partner_object(self):
        self.epcase.idf.copyidfobject(self.obj0)
        self.obj1 = self.epcase.idf.idfobjects[self.type_interzone][-1]
        self.obj1.Name =  f"{self.attrs.surface.partner_wall_name} {self.type_title}"
        self.obj1.Building_Surface_Name = self.attrs.surface.partner_wall_name

        self.obj1.Outside_Boundary_Condition_Object = self.obj0.Name
        self.obj0.Outside_Boundary_Condition_Object = self.obj1.Name

    # TODO get all objects of this type.. 


    # TODO be able to visualize doors in geometry .. 

        
        
    