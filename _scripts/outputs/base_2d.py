import plotly.graph_objects as go
from geometry.geometry_parser import GeometryParser
from dataclasses import dataclass

from helpers.plots import prepare_shape_dict, plot_shape


ZONE_COLOR = "#9dd1eb"
SUBSURFACE_COLOR = "#a32c54"
SHADINGS_COLOR = "#7bf542"

@dataclass
class Base2DPlotLimits:
    x_range: list
    y_range: list
    fig_width: int
    fig_height: int


class Base2DPlot:
    def __init__(self, geometry: GeometryParser, case_name) -> None:
        self.zones = geometry.zones
        self.subsurfaces = geometry.subsurfaces
        self.shadings = geometry.shadings
        self.case_name = case_name

    def run(self):
        self.make_traces()
        self.determine_plot_range()
        self.determine_figure_size()
        self.create_figure()

    def make_traces(self):
        self.traces = {}

        for zone in self.zones.values():
            self.traces[zone.bunch_name] = prepare_shape_dict(
                zone.polygon.exterior.coords,
                color=ZONE_COLOR,
                label=zone.display_name,
            )

        for subsurface in self.subsurfaces.values():
            self.traces[subsurface.bunch_name] = prepare_shape_dict(
                coords=subsurface.line.coords,
                type="line",
                color=SUBSURFACE_COLOR,
                label=subsurface.simple_object_type,
            )

        for shading in self.shadings.values():
            self.traces[shading.bunch_name] = prepare_shape_dict(
                shading.polygon.exterior.coords,
                color=SHADINGS_COLOR,
                label="",
            )

    def create_figure(self):
        self.limits = Base2DPlotLimits(self.x_range, self.y_range, self.fig_width, self.fig_height)
        self.fig = plot_shape(self.traces, **self.limits.__dict__, title=self.case_name)


    def determine_plot_range(self):
        buffer = 20
        min_x = min(self.get_vals("x0"))
        max_x = max(self.get_vals("x1"))

        min_y = min(self.get_vals("y0"))
        max_y = max(self.get_vals("y1"))

        self.x_range = [min_x - buffer, max_x + buffer]
        self.y_range = [min_y - buffer, max_y + buffer]

    def determine_figure_size(self, height=350):
        x_dif = self.x_range[1] - self.x_range[0]
        y_dif = self.y_range[1] - self.y_range[0]
        aspect = x_dif / y_dif

        self.fig_height = height
        self.fig_width = height * aspect

    def get_vals(self, ix_str):
        return [z[ix_str] for z in self.traces.values()]
