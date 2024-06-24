from geomeppy.patches import EpBunch
import shapely as sp


class Subsurface:
    def __init__(self, idf_data: EpBunch, wall) -> None:
        self.data = idf_data
        self.name = idf_data.Name
        self.wall = wall
        self.type = "" # object category or something.. 

        self.line: sp.LineString

    def create_display_name(self):
        self.display_name = f"{self.type} on {self.wall.display_name}"
        pass

    def get_geometry(self):
        self.start_x = self.data.Starting_X_Coordinate
        self.length = self.data.Length