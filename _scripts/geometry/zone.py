from geomeppy.patches import EpBunch
import shapely as sp

from geometry.wall import Wall
from outputs.classes import GeometryOutputData, TimeExtractData


class Zone:
    def __init__(self, idf_data:EpBunch, all_surfaces) -> None:
        self.data = idf_data
        self.name = idf_data.Name
        self.walls: list[Wall] = []
        self.all_surfaces = all_surfaces
        self.output_data = {}
        self.extracted_data = {}

        self.run()

    def __repr__(self):
        return f"Zone({self.name})"

    def run(self):
        self.get_walls()
        self.create_geometry()

    def get_walls(self, expected_walls=4):
        self.walls = [
            Wall(surface)
            for surface in self.all_surfaces
            if surface.Zone_Name == self.name and surface.Surface_Type == "wall"
        ]

        assert len(self.walls) == expected_walls, f"For zone {self.name}, added walls != expected walls"

    def create_geometry(self):
        wall_lines = [self.walls[i].line for i in range(4)]
        self.polygon = sp.get_geometry(sp.polygonize(wall_lines), 0)

        assert (
            type(self.polygon) == sp.Polygon
        ), "When creating zone geometry, zone was not polygonal "




    # dealing with outputs.. 

    def create_output_data(self, data: GeometryOutputData):
        self.output_data[data.short_name] = data

    def create_extracted_data(self, dataset_name, data: TimeExtractData):
        if dataset_name not in self.extracted_data.keys():
            self.extracted_data[dataset_name] = []
        self.extracted_data[dataset_name].append(data)


    def color_extracted_data(self, dataset_name, ix, color):
        self.extracted_data[dataset_name][ix].update_color(color)
