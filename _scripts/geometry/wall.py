from geomeppy.patches import EpBunch
import fnmatch
import re
import shapely as sp
from enum import Enum

from helpers.strings import get_last_word, test_intersecting_surface
from outputs.classes import GeometryOutputData


class CardinalDirection(Enum):
    # direction of outward normal of the wall..
    # https://eppy.readthedocs.io/en/latest/eppy.geometry.html#eppy.geometry.surface.azimuth
    NORTH = 0.0
    EAST = 90.0
    SOUTH = 180.0
    WEST = 270.0


class Wall:
    def __init__(self, idf_data: EpBunch, zone) -> None:
        self.data = idf_data
        self.name = idf_data.Name

        self.line: sp.LineString = None
        self.boundary_condition = None
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
        self.direction = CardinalDirection(self.data.azimuth).name

    def create_display_name(self):
        self.display_name = (
            f"Block {self.zone.entry_name} - {self.direction.title()} - W{self.number}"
        )
        self.bunch_name = (
            f"B_{self.zone.entry_name}_{self.direction.title()}_W{self.number}"
        )

    def get_geometry(
        self,
    ):
        # only care about coordinates 1 - 4
        z_coords = fnmatch.filter(self.data.fieldnames, "Vertex_[0-4]_Zcoordinate")

        # Define the regex pattern to match digits
        pattern = re.compile(r"\d+")

        vertices = []
        for fieldname in z_coords:
            # TODO will need to update this if do higher stories
            # get the vertex number where z-coord is 0
            if self.data[fieldname] == 0:
                # TODO figure out what is going on here / clean this up ..
                matches = pattern.findall(fieldname)
                # TODO some tests needed here..
                x_field = fnmatch.filter(
                    self.data.fieldnames, f"Vertex_{matches[0]}_Xcoordinate"
                )[0]
                x_val = self.data[x_field]

                y_field = fnmatch.filter(
                    self.data.fieldnames, f"Vertex_{matches[0]}_Ycoordinate"
                )[0]
                y_val = self.data[y_field]

                vertices.append([x_val, y_val])

        self.line = sp.LineString(vertices)

    # dealing with outputs
    def create_output_data(self, data: GeometryOutputData):
        self.output_data[data.short_name] = data
