import warnings

from methods.subsurfaces.surface_getter import SurfaceGetter
from methods.subsurfaces.inputs import (
    SubsurfaceCreatorInputs,
    SurfaceGetterInputs,
)
from methods.dynamic_subsurfaces.recreate_wall import WallRecreation
from methods.dynamic_subsurfaces.buffer import Buffer
from methods.dynamic_subsurfaces.placement import Placement

from methods.shadings.creator import ShadingCreator


class SubsurfaceCreator:
    def __init__(self, inputs: SubsurfaceCreatorInputs) -> None:
        self.inputs = inputs

    def run(self):
        for pair in self.inputs.ssurface_pairs:
            self.curr_pair = pair
            self.create_single_ssurface()

    def create_single_ssurface(self):
        self.get_case_surface()
        self.determine_ssurface_type()
        self.create_ssurface_name()
        self.initialize_object()
        try:
            self.calculate_start_coords()
        except:
            print(f"failed to create {self.name} on {self.surface}")
            self.abandon_object()
            return
        self.update_attributes()
        if self.surface.is_interior_wall:
            self.make_partner_object()
        self.add_shadings()

    def get_case_surface(self):
        input = SurfaceGetterInputs(self.inputs.zones, self.curr_pair)
        self.sg = SurfaceGetter(input)
        self.surface = self.sg.goal_surface

    def determine_ssurface_type(self):
        assert self.curr_pair.attrs
        self.type = self.curr_pair.attrs.object_type.name
        self.type_interzone = f"{self.type}:INTERZONE"
        self.type_title = self.type.title()

    def create_ssurface_name(self):
        self.name = f"{self.surface.name} {self.type_title}"

    def initialize_object(self):
        if self.surface.is_interior_wall:
            self.obj0 = self.inputs.case_idf.newidfobject(self.type_interzone)
        else:
            self.obj0 = self.inputs.case_idf.newidfobject(self.type)

    def update_attributes(self):
        self.obj0.Starting_X_Coordinate = self.start_x
        self.obj0.Starting_Z_Coordinate = self.start_z
        self.obj0.Height = self.height
        self.obj0.Length = self.width
        self.obj0.Construction_Name = self.curr_pair.attrs.construction.Name  # type: ignore
        self.obj0.Building_Surface_Name = self.surface.name
        self.obj0.Name = self.name

    def make_partner_object(self):
        self.obj1 = self.inputs.case_idf.copyidfobject(self.obj0)
        self.obj1.Name = f"{self.obj0.Name} Partner"
        self.obj1.Building_Surface_Name = self.surface.partner_wall_name

        self.obj1.Outside_Boundary_Condition_Object = self.obj0.Name
        self.obj0.Outside_Boundary_Condition_Object = self.obj1.Name

    def add_shadings(self):
        assert self.curr_pair.attrs
        if self.curr_pair.attrs.SHADING:
            if self.surface.is_interior_wall:
                warnings.warn(
                    f"Not adding shading to subsurface on interior wall - {self.surface.name}"
                )
                return
            self.shading_creator = ShadingCreator(self.name, self.inputs.case_idf)
            self.shading_creator.run()
