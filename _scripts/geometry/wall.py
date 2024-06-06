from geomeppy.patches import EpBunch
import fnmatch
import re
import shapely as sp
from enum import Enum

from helpers.helpers import get_last_word
from outputs.classes import GeometryOutputData

class CardinalDirection(Enum):
    # direction of outward normal of the wall..
    # https://eppy.readthedocs.io/en/latest/eppy.geometry.html#eppy.geometry.surface.azimuth
    NORTH = 0.0
    EAST = 90.0
    SOUTH = 180.0
    WEST = 270.0


class Wall:
    def __init__(self, idf_data:EpBunch) -> None:
        self.data = idf_data
        self.name = idf_data.Name

        self.line:sp.LineString = None
        self.boundary_condition = None
        self.output_data = {}

        self.run()


    def __repr__(self):
        return f"Wall({self.name2})"  

    def run(self):
        self.get_wall_number()
        self.get_direction()
        self.create_better_wall_name()
        self.get_geometry()

    def get_wall_number(self):
        self.number = get_last_word(self.name)

    def get_direction(self):
        self.direction = CardinalDirection(self.data.azimuth).name

    def create_better_wall_name(self):
        self.zone = self.name.split()[1]
        self.name2 = f"{self.zone}_{self.direction}"

    def get_geometry(self,):
        z_coords = fnmatch.filter(self.data.fieldnames, "Vertex_[0-4]_Zcoordinate")

        # Define the regex pattern to match digits
        pattern = re.compile(r"\d+")

        vertices = []
        for fieldname in z_coords:
            if self.data[fieldname] == 0:
                # get the vertex number where z-coord is 0
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