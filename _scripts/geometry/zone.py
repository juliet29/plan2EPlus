from geomeppy.patches import EpBunch
from munch import Munch
import shapely as sp

from geometry.wall import Wall
from outputs.classes import GeometryOutputData, TimeExtractData
from helpers.strings import to_python_format


class Zone:
    def __init__(self, zone_idf_data: EpBunch, case_idf) -> None:
        self.data = zone_idf_data
        self.name = zone_idf_data.Name
        self.wall_list: list[Wall] = []
        self.output_data = {}
        self.extracted_data = {}

        self.all_surfaces = case_idf.idfobjects["BUILDINGSURFACE:DETAILED"]

        self.run()

    def __repr__(self):
        return f"Zone({self.display_name})"

    def run(self):
        self.create_display_name()
        self.get_walls()
        self.create_geometry()

    def create_display_name(self):
        self.entry_name = self.name.split()[1]
        self.display_name = f"Block {self.entry_name}"
        self.bunch_name = f"B_{self.entry_name}"

    def get_walls(self):
        self.wall_list = [
            Wall(surface, self)
            for surface in self.all_surfaces
            if surface.Zone_Name == self.name and surface.Surface_Type == "wall"
        ]

        self.walls = Munch()
        for wall in self.wall_list:
            self.walls.update({wall.bunch_name: wall})

        print(f"Added {len(self.wall_list)} walls ")
        # assert len(self.walls) == expected_walls, f"For zone {self.name}, added walls != expected walls: {self.walls}"

    def create_geometry(self):
        wall_lines = [self.wall_list[i].line for i in range(len(self.wall_list))]
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
