from geomeppy.patches import EpBunch
import shapely as sp
from shapely import LineString




class Subsurface:
    def __init__(self, idf_data: EpBunch, wall) -> None:
        self.data = idf_data
        self.wall = wall

        self.create_display_name()
        self.get_geometry()

    def __repr__(self):
        return f"Subsurface({self.display_name})"

    def create_display_name(self):
        self.name = self.data.Name
        self.object_type = self.data.key.title()
        self.display_name = f"{self.object_type} on {self.wall.display_name}"
        pass

    def get_geometry(self):
        self.start_x = self.data.Starting_X_Coordinate
        self.length = self.data.Length
        line = self.wall.line
        start =line.line_interpolate_point(self.start_x)
        end = line.line_interpolate_point(self.start_x+self.length)
        self.line = LineString([start, end])
