from geomeppy.patches import EpBunch
import shapely as sp

from geometry.wall_normal import WallNormal
from helpers.strings import test_intersecting_surface
from geometry.surface_geom import SurfaceGeometryExtractor
from geometry.subsurface import Subsurface


class Wall:
    def __init__(self, idf_data: EpBunch, zone) -> None:
        self.data = idf_data
        self.name = idf_data.Name

        self.line: sp.LineString
        self.output_data = {}
        self.zone = zone

        self.is_intersecting_wall = False
        self.is_interior_wall = False
        self.partner_wall_name = None

        self.run()

    def __repr__(self):
        return f"Wall({self.display_name})"

    def run(self):
        self.handle_interior_wall()
        self.get_wall_number()
        self.get_direction()
        self.create_display_name()
        self.get_geometry()

    def handle_interior_wall(self):
        if test_intersecting_surface(self.name):
            self.is_intersecting_wall = True
            if self.data.Outside_Boundary_Condition == "surface":
                self.is_interior_wall = True
                self.partner_wall_name = self.data.Outside_Boundary_Condition_Object

    def get_wall_number(self):
        if self.is_intersecting_wall:
            self.number = self.name[-4:]
        else:
            self.number = self.name[-2:]

    def get_direction(self):
        self.direction = WallNormal(self.data.azimuth).name

    def create_display_name(self):
        self.display_name = (
            f"Block {self.zone.entry_name} - {self.direction.title()} - W{self.number}"
        )
        self.bunch_name = (
            f"B_{self.zone.entry_name}_{self.direction.title()}_W{self.number}"
        )
        self.short_name = f"B{self.zone.entry_name}-W{self.number}"

    def get_geometry(self):
        sg = SurfaceGeometryExtractor(self)
        # getting the line that defines the base of this wall..
        vertices = []
        for coord in sg.surface_geom.values():
            if coord.Z == 0:
                vertices.append([coord.X, coord.Y])

        assert len(vertices) == 2, f"Line defining surface {self.display_name} ! have 2 vertices: {vertices}"

        self.line = sp.LineString(vertices)
        # print([c for c in self.line.coords])



    # get subsurfaces 
    def get_subsurfaces(self, subsurfaces):
        self.ssurface_list = [Subsurface(s, self) for s in subsurfaces if s.Building_Surface_Name == self.name]
