from shapely import Point, Polygon

from geometry.wall import Wall, WallNormal
from helpers.shapely_helpers import get_coords_as_points
from case_edits.methods.dynamic_subsurfaces.surface_polygon import SurfacePolygon



class WallRecreation:
    def __init__(self, wall:Wall, room_height=10) -> None:
        self.wall = wall 
        self.room_height= room_height
        self.run()

    def run(self):
        self.get_coords()
        self.create_wall()

    def get_coords(self):
        self.coords = get_coords_as_points(self.wall.line.coords)
        assert len(self.coords) == 2

    def create_wall(self):
        if self.is_x_dir():
            self.sort_coords_x()

        elif self.is_y_dir():
            print("y dir")
            self.sort_coords_y()
            self.transform_y_coords()

        self.create_polygon()
    

    def create_polygon(self):
        c1 =  tuple([i[0] for i in self.coords[0].xy])
        c2 = tuple([i[0] for i in self.coords[1].xy])

        c3 = (self.coords[1].x, self.coords[1].y + self.room_height)
        c4 = (self.coords[0].x, self.coords[0].y + self.room_height)

        polygon = Polygon([c1, c2, c3, c4, c1])

        self.polygon = SurfacePolygon(polygon)



    def transform_y_coords(self):
        length = self.wall.line.length
        new_coord = Point(self.coords[0].x + length, self.coords[0].y)
        self.coords[1] = new_coord

    def sort_coords_x(self):
        self.coords = sorted(self.coords, key=lambda pt: pt.x)
    
    def sort_coords_y(self):
        self.coords = sorted(self.coords, key=lambda pt: pt.y)


    def is_x_dir(self):
        if self.wall.direction == WallNormal.NORTH.name or self.wall.direction == WallNormal.SOUTH.name:
            assert self.double_check_direction() == (True, False)
            return True
        
    def is_y_dir(self):
        if self.wall.direction == WallNormal.EAST.name or self.wall.direction == WallNormal.WEST.name:
            assert self.double_check_direction() == (False, True)
            return True

    def double_check_direction(self):
        dif_x = bool(self.coords[0].x - self.coords[1].x)
        dif_y = bool(self.coords[0].y - self.coords[1].y)
        return (dif_x, dif_y)