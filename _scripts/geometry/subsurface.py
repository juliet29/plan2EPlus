from eppy.bunch_subclass import EpBunch
from shapely import LineString

from geometry.shading import Shading


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
        self.get_simple_object()
        self.display_name = f"{self.simple_object_type} on {self.wall.display_name}"
        self.bunch_name = f"{self.simple_object_type}_{self.wall.bunch_name}"
        self.short_name = f"{self.simple_object_type}-W{self.wall.number}"

    def get_geometry(self):
        self.start_x = self.data.Starting_X_Coordinate
        self.length = self.data.Length
        line = self.wall.line
        start = line.line_interpolate_point(self.start_x)
        end = line.line_interpolate_point(self.start_x + self.length)
        self.line = LineString([start, end])

    def get_simple_object(self):
        self.object_type = self.data.key.title()
        if "interzone" in self.object_type.lower():
            self.simple_object_type = self.object_type.split(":")[0]
        else:
            self.simple_object_type = self.object_type

    def assign_shading(self, shading_object):
        self.shading = Shading(shading_object, self)
        return self.shading
