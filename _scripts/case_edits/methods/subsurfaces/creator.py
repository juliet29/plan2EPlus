from case_edits.methods.subsurfaces.surface_getter import SurfaceGetter
from case_edits.methods.subsurfaces.inputs import (
    SubsurfaceInputs,
    SurfaceGetterInputs,
    DOOR_GAP,
)


class SubsurfaceCreator:
    def __init__(self, inputs: SubsurfaceInputs) -> None:
        self.inputs = inputs
        self.attrs = self.inputs.attributes

    # TODO check attrs width and height attrs.less than wall width and (height + DOOR_GAP)

    def create_all_ssurface(self):
        for pair in self.inputs.ssurface_pairs:
            self.curr_pair = pair
            self.create_single_ssurface()

    def create_single_ssurface(self):
        self.get_case_surface()
        self.determine_ssurface_type()
        self.create_ssurface_name()
        self.calculate_start_coords()
        self.initialize_object()
        self.update_attributes()
        if self.surface.is_interior_wall:
            self.make_partner_object()

    def get_case_surface(self):
        input = SurfaceGetterInputs(self.inputs.zones, self.curr_pair)
        self.sg = SurfaceGetter(input)
        self.surface = self.sg.goal_surface

    def determine_ssurface_type(self):
        self.type = self.attrs.object_type.name
        self.type_interzone = f"{self.type}:INTERZONE"
        self.type_title = self.type.title()

    def create_ssurface_name(self):
        self.name = f"{self.surface.name} {self.type_title}"
        # TODO check that no other object with this name, 
        # TODO what if its an interzone ssurface?
        # i think this is redundant..

    def calculate_start_coords(self):
        surface_center = int(self.surface.data.width) / 2
        half_length = self.attrs.length / 2
        self.start_x = surface_center - half_length
        self.start_z = DOOR_GAP  # TODO adjust for windeows  !

    def initialize_object(self):
        if self.surface.is_interior_wall:
            self.obj0 = self.inputs.case_idf.newidfobject(self.type_interzone)
        else:
            self.obj0 = self.inputs.case_idf.newidfobject(self.type)

    def update_attributes(self):
        self.obj0.Starting_X_Coordinate = self.start_x
        self.obj0.Starting_Z_Coordinate = self.start_z
        self.obj0.Height = self.attrs.height
        self.obj0.Length = self.attrs.length
        self.obj0.Construction_Name = self.attrs.construction.Name
        self.obj0.Building_Surface_Name = self.surface.name
        self.obj0.Name = self.name

    def make_partner_object(self):
        self.obj1 = self.inputs.case_idf.copyidfobject(self.obj0)
        # self.inputs.case_idf.idfobjects[self.type_interzone][-1]
        self.obj1.Name = f"{self.obj0.Name} Partner"
        self.obj1.Building_Surface_Name = self.surface.partner_wall_name

        self.obj1.Outside_Boundary_Condition_Object = self.obj0.Name
        self.obj0.Outside_Boundary_Condition_Object = self.obj1.Name


