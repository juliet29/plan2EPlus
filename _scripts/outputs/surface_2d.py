import plotly.graph_objects as go
import plotly.express as px

from outputs.input_classes import Surface2DPlotInputs
from outputs.helpers import create_plot_title
from helpers.helpers import min_max_norm
from helpers.plot_colors import get_norm_plotly_colors
from helpers.plots import prepare_shape_dict, plot_shape, create_colorbar


class Surface2DPlot:
    def __init__(self, inputs: Surface2DPlotInputs) -> None:
        self.inputs = inputs
        self.color_scheme = px.colors.diverging.Portland
        self.used_walls = []

    def create_plot(self):
        self.create_traces()
        self.fig = plot_shape(
            self.trace_dict,
            self.inputs.base2D.limits.x_range,
            self.inputs.base2D.limits.y_range,
            padding=80,
        )
        self.fig.add_trace(self.colorbar)

        self.create_title()
        self.fig.update_layout(title_text=self.title)

    def create_traces(self):
        self.prepare_for_traces()
        self.trace_dict = {}
        for key, surface in self.surface_map.items():
            label = self.create_labels(surface)
            color = self.get_trace_color(self.values_dict[key])
            self.trace_dict[key] = prepare_shape_dict(surface.line.coords, label=label, color=color, type="line")  # type: ignore

        self.colorbar = create_colorbar(
            self.min_val, self.max_val, color_scheme=self.color_scheme  # type: ignore
        )

    def prepare_for_traces(self):
        self.arrange_collection()
        self.match_surfaces()
        self.get_values()

    def arrange_collection(self):
        self.collection_dict = {
            o.header.metadata["Surface"]: o for o in self.inputs.collection_by_ap
        }

    def match_surfaces(self):
        collection_surfaces = self.collection_dict.keys()
        self.surface_map = {}

        for zone in self.inputs.geometry.zones.values():
            for wall in zone.walls.values():
                if wall.name.upper() in collection_surfaces:
                    self.surface_map[wall.name.upper()] = wall

        for subsurface in self.inputs.geometry.subsurfaces.values():
            if subsurface.name.upper() in collection_surfaces:
                self.surface_map[subsurface.name.upper()] = subsurface



    def get_values(self):
        self.values_dict = {}
        for key in self.surface_map.keys():
            self.values_dict[key] = self.get_value_by_time(
                self.collection_dict[key], self.inputs.plot_time
            )

        self.max_val = max(self.values_dict.values())
        self.min_val = min(self.values_dict.values())

    def get_value_by_time(self, collection, plot_time):
        for ix, t in enumerate(collection.datetimes):
            if t.time == plot_time:
                return round(collection.values[ix], 2)
        raise Exception(
            f"{plot_time} is an invalid time. Timestep is every {60/collection.header.analysis_period.timestep} mins!!"
        )

    def get_trace_color(self, val):
        norm_val = min_max_norm(val, self.min_val, self.max_val)
        color = get_norm_plotly_colors(norm_val, self.min_val, self.max_val, color_scheme=self.color_scheme)[0]  # type: ignore
        return color
    
    def create_labels(self, surface):
        try:
            # windows / doors never
            surface.wall.short_name
            label = ""
        except:
            label = surface.short_name

        return label
    
    def create_title(self):
        self.title = create_plot_title(self.inputs.collection_by_ap[0])
        time_str = self.inputs.plot_time.strftime("%H:%M")
        self.time_title = f"<sup>- Time = {time_str} </sup>"
        self.title = self.title + self.time_title
