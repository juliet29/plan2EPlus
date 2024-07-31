from dataclasses import dataclass
from methods.dynamic_subsurfaces.surface_polygon import SurfacePolygon
from shapely import Point, Polygon
from methods.dynamic_subsurfaces.inputs import NinePoints, MutablePoint



# takes the bufferered_surface 
class NinePointsCreator:
    def __init__(self, surface:SurfacePolygon) -> None:
        self.coords = surface.organized_coords
        self.dimensions = surface.dimensions
        self.make_nine_points()

    def make_nine_points(self):
        self.init_points()
        self.assign_corners()
        self.assign_middles()

    def init_points(self):
        temp = [Point(0,0)] * 9
        self.points = NinePoints(*temp)

    def assign_corners(self):
        self.points.bottom_left = self.coords.bottom_left
        self.points.bottom_right = self.coords.bottom_right
        self.points.top_left = self.coords.top_left
        self.points.top_right = self.coords.top_right

    def assign_middles(self):
        half_width = self.dimensions.width / 2
        half_height = self.dimensions.height / 2
        x0 = self.points.bottom_left.x
        y0 = self.points.bottom_left.y

        self.points.middle_middle = Point(x0 + half_width, y0 + half_height)

        self.points.bottom_middle = Point(self.points.middle_middle.x, self.points.bottom_left.y)

        self.points.top_middle = Point(self.points.middle_middle.x, self.points.top_left.y)

        self.points.middle_left = Point(self.points.bottom_left.x, self.points.middle_middle.y)

        self.points.middle_right = Point(self.points.bottom_right.x, self.points.middle_middle.y)

    