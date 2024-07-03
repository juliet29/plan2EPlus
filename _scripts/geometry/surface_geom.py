from dataclasses import dataclass
from munch import Munch
from pprint import pprint, pformat
# from geometry.wall import Wall
import re

"""this is a helper for wall.py"""

@dataclass
class Coordinate:
    X: float
    Y: float
    Z: float


class SurfaceGeometryExtractor:
    def __init__(self, surface) -> None:
        # TODO specify that the type of the surrface is wall-like ..
        self.name = surface.display_name
        self.surface = surface.data
        self.surface_geom = Munch()
        self.run()
    
    def __repr__(self):
        return f"{self.name} \n {pformat(self.surface_geom)}"


    def run(self):
        # fieldname keys look like: Vertex_1_Xcoordinate
        # getting the digit
        self.pattern = re.compile("([0-9]+)")

        self.create_geom_structure()
        self.populate_geom_structure()

    def create_geom_structure(self):
        for fieldname in self.surface.fieldnames:
            if self.is_valid_fieldname(fieldname):
                self.vertex_name = self.pattern.search(fieldname).group(0)  # type: ignore
                self.update_geom_structure()

    def populate_geom_structure(self):
        for vertex_num in self.surface_geom.keys():
            self.create_coordinate_keys(vertex_num)
            # also potentially shapely point.. 
            self.surface_geom[vertex_num] = Coordinate(
                self.surface[self.x_key],
                self.surface[self.y_key],
                self.surface[self.z_key],
            )

    def is_valid_fieldname(self, fieldname):
        if "coordinate" in fieldname:
            if self.surface[fieldname] != str():
                return True

    def update_geom_structure(self):
        if self.vertex_name not in self.surface_geom.keys():
            self.surface_geom[self.vertex_name] = Coordinate(0, 0, 0)

    def create_coordinate_keys(self, vertex_num):
        self.x_key = f"Vertex_{vertex_num}_Xcoordinate"
        self.y_key = f"Vertex_{vertex_num}_Ycoordinate"
        self.z_key = f"Vertex_{vertex_num}_Zcoordinate"
