from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
# from outputs.plotter import Plotter
from helpers.plots import plot_rectangle_shape


class Base2DPlot:
    def __init__(self, PlotterObj) -> None:
        self.plotter = PlotterObj
        self.zones  = self.plotter.inputs.geometry.zones


    def run(self):
        self.make_traces_dict()
        self.determine_plot_range()
        self.determine_figure_size()
        self.create_figure()
        self.update_figure_layout()
        self.fig.show()

    def make_traces_dict(self):
        self.plot_dict = {}
        for zone in self.zones.values():
            self.plot_dict[zone.bunch_name] = plot_rectangle_shape(zone.polygon)

    def determine_plot_range(self):
        buffer = 20
        min_x = min(self.get_vals("x0"))
        max_x = max(self.get_vals("x1"))

        min_y = min(self.get_vals("y0"))
        max_y = max(self.get_vals("y1"))

        self.x_range = [min_x - buffer, max_x + buffer]
        self.y_range = [min_y - buffer, max_y + buffer]


    def determine_figure_size(self, height=400):
        x_dif = self.x_range[1] - self.x_range[0]
        y_dif = self.y_range[1] - self.y_range[0]
        aspect = x_dif / y_dif

        self.fig_height = height
        self.fig_width = height * aspect


    def create_figure(self):
        self.fig = go.Figure()
        for trace in self.plot_dict.values():
            self.fig.add_shape(**trace)
        self.fig.update_xaxes(range=self.x_range)
        self.fig.update_yaxes(range=self.y_range)

    def update_figure_layout(self, padding=50):
        self.fig.update_layout(
            autosize=False,
            width=self.fig_width,
            height=self.fig_height,
            margin=dict(
                l=padding,
                r=padding,
                b=padding,
                t=padding,
                pad=4 #TODO what is pad?
            ),
        )



    def get_vals(self, ix_str):
        return [z[ix_str] for z in self.plot_dict.values()]