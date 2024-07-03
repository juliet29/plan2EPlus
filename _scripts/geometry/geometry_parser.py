import plotly.graph_objects as go
from geomeppy import IDF
from munch import Munch

from geometry.zone import Zone
from helpers.plots import get_plotly_colors, plot_polygon, plot_line_string

# from helpers.strings import to_python_format


class GeometryParser:
    def __init__(self, idf: IDF) -> None:
        self.idf = idf
        self.get_zones()
        self.subsurfaces = Munch()

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

    def plot_zones(self):
        self.prepare_to_plot_zones()

        self.fig = go.Figure()
        for t in self.traces:
            self.fig.add_trace(t)
        self.fig.show()

    def prepare_to_plot_zones(self):
        _, color_iterator = get_plotly_colors()

        self.traces = []

        for zone in self.zone_list:
            color = next(color_iterator)
            trace = plot_polygon(zone.polygon, color=color, label=zone.display_name)
            self.traces.append(trace)

            for wall in zone.wall_list:
                trace = plot_line_string(wall.line, color=color, label=f"{wall.display_name}")
                self.traces.append(trace)
