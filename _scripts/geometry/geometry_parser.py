import plotly.graph_objects as go
from geomeppy import IDF
from munch import Munch

from geometry.zone import Zone

# from helpers.strings import to_python_format


class GeometryParser:
    def __init__(self, idf: IDF) -> None:
        self.idf = idf
        self.get_zones()
        self.subsurfaces = Munch()
        self.walls = Munch()

    def get_zones(self):
        self.check_zone_names_are_unique()
        self.zone_list = [Zone(zone, self.idf) for zone in self.idf.idfobjects["ZONE"]]

        self.zones = Munch()
        for zone in self.zone_list:
            self.zones.update({zone.bunch_name: zone})

    def check_zone_names_are_unique(self):
        zone_names = [zone.Name for zone in self.idf.idfobjects["ZONE"]]
        assert len(set(zone_names)) == len(
            zone_names
        ), f"Zone names are not unique: {zone_names}"

   