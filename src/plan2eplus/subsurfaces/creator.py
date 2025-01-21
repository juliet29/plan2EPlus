from copy import deepcopy
from geomeppy import IDF

from subsurfaces.constructions import assign_default_constructions
from helpers.ep_helpers import is_interior_wall, create_partner_name
from subsurfaces.interfaces import SubsurfacePair

from subsurfaces.logic import (
    create_starting_coord,
    get_approp_surface_and_attrs,
)


class SubsurfaceCreator:
    def __init__(
        self,
        idf: IDF,
        pair: SubsurfacePair,
    ) -> None:
        self.idf = idf
        self.pair = pair
        self.is_interior_wall = False

    def run(self):
        self.get_surface_and_update_attrs()
        self.get_start_location()
        self.create_objects()

    def get_surface_and_update_attrs(self):
        self.surface, self.attrs = get_approp_surface_and_attrs(self.idf, self.pair)
        # print(self.attrs.object_type)
        # self.attrs = assign_default_constructions(self.idf, self.attrs)
        # print(self.attrs.construction)

    def get_start_location(self):
        self.start_width, self.start_height = create_starting_coord(
            self.surface, self.attrs.dimensions, self.attrs.location_in_wall.name
        )

    def create_objects(self):
        self.gather_details()
        self.initialize_object()
        self.update_attributes()
        if self.is_interior_wall:
            self.make_partner_object()

    def gather_details(self):
        self.object_type = self.pair.attrs.object_type.name
        self.type_interzone = f"{self.object_type}:INTERZONE"
        self.name = f"{self.surface.Name} {self.object_type.title()}"

    def initialize_object(self):
        self.is_interior_wall = is_interior_wall(self.surface)
        if self.is_interior_wall:
            self.obj0 = self.idf.newidfobject(self.type_interzone)
        else:
            self.obj0 = self.idf.newidfobject(self.object_type)

    def update_attributes(self):
        width, height = self.attrs.dimensions
        self.obj0.Starting_X_Coordinate = self.start_width
        self.obj0.Starting_Z_Coordinate = self.start_height
        self.obj0.Length = width
        self.obj0.Height = height
        self.obj0.Building_Surface_Name = self.surface.Name
        self.obj0.Name = self.name

        # assert self.attrs.construction
        self.obj0.Construction_Name = "" #self.attrs.construction.Name

    def make_partner_object(self):
        self.obj1 = self.idf.copyidfobject(self.obj0)
        self.obj1.Name = create_partner_name(self.obj0.Name)
        self.obj1.Building_Surface_Name = self.surface.Outside_Boundary_Condition_Object

        self.obj1.Outside_Boundary_Condition_Object = self.obj0.Name
        self.obj0.Outside_Boundary_Condition_Object = self.obj1.Name


def add_subsurfaces_to_case(_idf: IDF, pairs: list[SubsurfacePair]):
    idf = deepcopy(_idf)
    for pair in pairs:
        sc = SubsurfaceCreator(idf=idf, pair=pair)
        sc.run()
        idf = sc.idf
    return idf
