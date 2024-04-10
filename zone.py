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
        # walls are differentiated from floors / cielings because they have 2 different z values within their coordinates.

        zone_surfaces = [
            surface for surface in self.all_surfaces if surface.Zone_Name == self.name
        ]

        for surface in zone_surfaces:
            # get fieldnames for the z coordinates
            valid_fieldnames = fnmatch.filter(
                surface.fieldnames, f"Vertex_[0-{expected_walls}]_Zcoordinate"
            )

            # check that we have 2 different z coordinates
            valid_values = []
            for fieldname in valid_fieldnames:
                valid_values.append(surface[fieldname])
            if len(set(valid_values)) == 2:
                self.walls.append(Wall(surface))
                
        ic(len(self.walls))

        assert len(self.walls) == expected_walls, "Added walls != expected walls"

    def create_geometry(self):
        wall_lines = [self.walls[i].line for i in range(4)]
        self.polygon = sp.get_geometry(sp.polygonize(wall_lines),0)

        assert type(self.polygon) == sp.Polygon, "When creating zone geometry, zone was not polygonal "
