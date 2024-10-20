
from geomeppy import IDF

from new_subsurfaces.ep_helpers import is_interior_wall
from new_subsurfaces.interfaces import SubsurfacePair

from new_subsurfaces.preparation import create_starting_coord, get_approp_surface_and_attrs


class SubsurfaceCreator:
    def __init__(self, pair: SubsurfacePair, idf: IDF) -> None:
        self.pair = pair
        self.idf = idf

    def run(self):
        self.get_surface_and_update_attrs()
        self.gather_details()
        self.initialize_object()
        self.update_attributes()
        self.make_partner_object()
  

    def get_surface_and_update_attrs(self):
        self.surface, self.attrs = get_approp_surface_and_attrs(self.idf, self.pair)

    def gather_details(self):
        self.object_type = self.pair.attrs.object_type.name
        self.type_interzone = f"{self.object_type}:INTERZONE"
        self.name = f"{self.surface.name} {self.object_type.title()}"

    def initialize_object(self):
        if is_interior_wall(self.surface):
            self.obj0 = self.idf.newidfobject(self.type_interzone)
        else:
            self.obj0 = self.idf.newidfobject(self.object_type)

    def update_attributes(self):
        self.obj0.Building_Surface_Name = self.surface.name
        self.obj0.Name = self.name

        start_width, start_height = create_starting_coord(self.surface, self.attrs.dimensions, self.attrs.location_in_wall.name)
        width, height = self.attrs.dimensions
        self.obj0.Starting_X_Coordinate = start_width
        self.obj0.Starting_Z_Coordinate = start_height
        self.obj0.Length = width
        self.obj0.Height = height
        
        self.obj0.Construction_Name = self.curr_pair.attrs.construction.Name  # type: ignore

    def make_partner_object(self):
        self.obj1 = self.idf.copyidfobject(self.obj0)
        self.obj1.Name = f"{self.obj0.Name} Partner"
        self.obj1.Building_Surface_Name = self.surface.partner_wall_name

        self.obj1.Outside_Boundary_Condition_Object = self.obj0.Name
        self.obj0.Outside_Boundary_Condition_Object = self.obj1.Name

    # def add_shadings(self):
    #     assert self.curr_pair.attrs
    #     if self.curr_pair.attrs.SHADING:
    #         if self.surface.is_interior_wall:
    #             warnings.warn(
    #                 f"Not adding shading to subsurface on interior wall - {self.surface.name}"
    #             )
    #             return
    #         self.shading_creator = ShadingCreator(self.name, self.inputs.case_idf)
    #         self.shading_creator.run()
