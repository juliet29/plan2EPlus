import plotly.graph_objects as go
from geomeppy import IDF
from munch import Munch

from geometry.zone import Zone

# from helpers.strings import to_python_format


class GeometryParser:
    def __init__(self, idf: IDF) -> None:
        self.idf = idf
        self._get_zones()
        self.shadings = Munch()
        self.subsurfaces = Munch()
        self.walls = Munch()

    def _get_zones(self):
        self._check_zone_names_are_unique()

        self.zone_list = []
        for zone in self.idf.idfobjects["ZONE"]:
            try:
                self.zone_list.append(Zone(zone, self.idf))
            except:
                print(f"zone failed: {zone.Name}")

        self.zones = Munch()
    
        for zone in self.zone_list:
            self.zones.update({zone.bunch_name: zone})
        

    def _check_zone_names_are_unique(self):
        zone_names = [zone.Name for zone in self.idf.idfobjects["ZONE"]]
        assert len(set(zone_names)) == len(
            zone_names
        ), f"Zone names are not unique: {zone_names}"

    def update_geometry_walls(self):
        for zone in self.zones.values():
            self.walls.update(zone.walls)

    def update_geometry_subsurfaces(self):
        subsurfaces = []
        for zone in self.zones.values():
            subsurfaces.extend(zone.get_subsurfaces())
        for subsurface in subsurfaces:
            self.subsurfaces.update({subsurface.bunch_name: subsurface})
        self.update_geometry_shadings()
   
    def update_geometry_shadings(self):
        idf_shadings = self.idf.idfobjects["SHADING:OVERHANG"]
        for s in idf_shadings:
            ssurface_name = s.Name.split(" Shading")[0]
            ssurface = [v for v in self.subsurfaces.values() if v.name == ssurface_name][0]
            shading = ssurface.assign_shading(s)
            self.shadings.update({shading.bunch_name: shading})

