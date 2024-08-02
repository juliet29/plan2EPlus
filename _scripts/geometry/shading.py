from shapely import Point, Polygon

from geomeppy.patches import EpBunch

from geometry.wall_normal import WallNormal
from helpers.shapely_helpers import get_coords_as_points, get_point_as_xy

from warnings import warn
# from geometry.subsurface import Subsurface


class Shading:
    def __init__(self, idf_data: EpBunch, subsurface) -> None:
        self.data = idf_data
        self.subsurface = subsurface
        self.display_bias = 1
        self.run()

    def __repr__(self):
        return f"Shading({self.display_name})"

    def run(self):
        self.create_display_name()
        self.get_geometry()

    def create_display_name(self):
        self.name = self.data.Name
        self.get_simple_object()
        self.display_name = (
            f"{self.simple_object_type} on {self.subsurface.display_name}"
        )
        self.bunch_name = f"{self.simple_object_type}_{self.subsurface.bunch_name}"
        self.short_name = f"{self.simple_object_type}_W{self.subsurface.wall.number}"

    def get_simple_object(self):
        self.object_type = self.data.key.title()
        if "overhang" in self.object_type.lower():
            self.simple_object_type = self.object_type.split(":")[0]
        else:
            self.simple_object_type = self.object_type

    def get_geometry(self):
        self.original_points = get_coords_as_points(self.subsurface.line.coords)
        self.depth = float(self.data.Depth) * self.display_bias
        fx = self.create_new_coords_fx(self.subsurface.wall.direction)
        self.new_points = [fx(p) for p in self.original_points]
        self.new_points.reverse()
        coords = [get_point_as_xy(c) for c in (self.original_points + self.new_points)]
        self.polygon = Polygon(coords)

        

    def check_valid_geometry(self):
        is_valid_geom = self.polygon.is_valid
        if not is_valid_geom:
            warn(f"shading polygon `{self.name}` is invalid")

    def create_new_coords_fx(self, direction):
        match direction:
            case WallNormal.NORTH.name:
                return lambda pt: Point(pt.x, pt.y + self.depth)
            case WallNormal.SOUTH.name:
                return lambda pt: Point(pt.x, pt.y - self.depth)
            case WallNormal.EAST.name:
                return lambda pt: Point(pt.x + self.depth, pt.y)
            case WallNormal.WEST.name:
                return lambda pt: Point(pt.x - self.depth, pt.y)
            case _:
                raise Exception(f"Invalid Case - {direction}")
