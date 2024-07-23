from shapely import Point, Polygon

from case_edits.methods.dynamic_subsurfaces.surface_polygon import SurfacePolygon
from case_edits.methods.dynamic_subsurfaces.nine_points import NinePointsCreator


class Buffer:
    def __init__(self, surface:SurfacePolygon) -> None:
        self.original_surface = surface
        self.run()

    def run(self):
        self.get_buffer_distance()
        self.create_buffer_polygon()
        self.assign_nine_points()

    def get_buffer_distance(self):
        dims = self.original_surface.dimensions
        smaller_dim = dims.width if dims.width < dims.height else dims.height
        self.buffer_dist = smaller_dim*0.1


    def create_buffer_polygon(self):
        p1, p2, p3, p4, _ = self.original_surface.organized_coords.coords_list #ccw starting from bottom left 
        p1n = (p1.x + self.buffer_dist, p1.y + self.buffer_dist)
        p2n = (p2.x - self.buffer_dist, p2.y + self.buffer_dist)
        p3n = (p3.x - self.buffer_dist, p3.y - self.buffer_dist)
        p4n = (p4.x + self.buffer_dist, p4.y - self.buffer_dist)

        polygon = Polygon([p1n, p2n, p3n, p4n, p1n])
        self.polygon = SurfacePolygon(polygon)

    def assign_nine_points(self):
        self.npc = NinePointsCreator(self.polygon)
        self.nine_points = self.npc.points




  