from helpers import *
from zone import *


class GeometryParser:
    def __init__(self, idf) -> None:
        self.idf = idf

    def run(self):
        self.get_zones()

    def get_zones(self):
        all_surfaces = self.idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        self.zones = [Zone(i, all_surfaces) for i in self.idf.idfobjects["ZONE"]]

    def plot_zones(self):
        self.prepare_to_plot_zones()
        self.fig = go.Figure()
        for t in self.traces:
            self.fig.add_trace(t)

        self.fig.show()

    def prepare_to_plot_zones(self):
        self.traces = []
        for zone in self.zones:
            for wall in zone.walls:
                trace = plot_line_string(wall.line)
                self.traces.append(trace)
