from helpers import *
from wall import *

class Zone:
    def __init__(self, idf_data:EpBunch, all_surfaces) -> None:
        self.data = idf_data
        self.name = idf_data.Name
        self.walls:list[Wall] = [] 
        self.all_surfaces = all_surfaces
        
        self.run()

    def __repr__(self):
        return f"Zone({self.name})"
    
    def run(self):
        self.get_walls()
        self.create_geometry()
    

    def get_walls(self,  expected_walls=4):
        self.walls = [Wall(surface) for surface in self.all_surfaces if surface.Zone_Name == self.name and surface.Surface_Type == "wall"]

        assert len(self.walls) == expected_walls, "Added walls != expected walls"


    def create_geometry(self):
        wall_lines = [self.walls[i].line for i in range(4)]
        self.polygon = sp.get_geometry(sp.polygonize(wall_lines),0)

        assert type(self.polygon) == sp.Polygon, "When creating zone geometry, zone was not polygonal "
