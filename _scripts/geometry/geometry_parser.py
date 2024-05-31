import plotly.graph_objects as go

from geometry.zone import Zone
from helpers.plots import get_plotly_colors, plot_polygon, plot_line_string



class GeometryParser:
    def __init__(self, idf) -> None:
        self.idf = idf


    def get_zones(self):
        self.check_zone_names_are_unique()

        all_surfaces = self.idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        self.zones = [Zone(i, all_surfaces) for i in self.idf.idfobjects["ZONE"]]


    def check_zone_names_are_unique(self):
        zone_names = [i.Name for i in self.idf.idfobjects["ZONE"]]
        assert len(set(zone_names)) == len(zone_names), f"Zone names are not unique: {zone_names}"


    def plot_zones(self):
        self.prepare_to_plot_zones()

        self.fig = go.Figure()
        for t in self.traces:
            self.fig.add_trace(t)
        self.fig.show()


    def prepare_to_plot_zones(self):
        _, color_iterator = get_plotly_colors()

        self.traces = []

        for zone in self.zones:
            color = next(color_iterator)
            trace = plot_polygon(zone.polygon, color=color, label=zone.name)
            self.traces.append(trace)

            for wall in zone.walls:
                trace = plot_line_string(wall.line, color=color, label=f"Wall {wall.number}")
                self.traces.append(trace)

