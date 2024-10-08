from plotly.subplots import make_subplots
import plotly.express as px


from outputs.classes import TimeExtractData


from helpers.helpers import min_max_norm
from helpers.plot_colors import   get_norm_plotly_colors,create_colorbar
from helpers.plots import (
    prepare_polygon_trace,
    prepare_line_traces,
    prepare_shape_dict,
)


class SpaceTimePlot:
    def __init__(self, PlotterObj) -> None:
        self.plotter = PlotterObj
        self.color_scheme = px.colors.sequential.RdBu_r

        self.spatial_values = []

    def extract_many_times(self, times, dataset_name):
        self.dataset_name = dataset_name
        self.plotter.check_dataset_is_zonal(self.dataset_name)

        self.candidate_times = times
        self.get_dataset_datetimes()
        self.get_time_indices()

        for ix in self.time_indices:
            self.extract_time_data(ix)

    def get_dataset_datetimes(self):
        dataset = self.plotter.zone_list[0].output_data[self.dataset_name].dataset
        self.datetimes = dataset.datetimes
        self.timestep = dataset.timestep_text

    def get_time_indices(self):
        self.time_indices = []
        for candidate_time in self.candidate_times:
            self.return_valid_time(candidate_time)

    def return_valid_time(self, candidate_time):
        for ix, datetime in enumerate(self.datetimes):
            if candidate_time == datetime.time:
                self.time_indices.append(ix)
                return
        raise Exception(
            f"{candidate_time} is an invalid time. Timestep is {self.timestep}!!"
        )

    def extract_time_data(self, time_index):
        for zone in self.plotter.zone_list:
            value = round(
                zone.output_data[self.dataset_name].dataset.values[time_index], 2
            )
            self.spatial_values.append(value)

            data = TimeExtractData(value, time_index)
            zone.create_extracted_data(self.dataset_name, data)

    def create_spatial_plots(self):
        self.prepare_spatial_colors()
        self.prepare_spatial_plots()

        titles = [i.strftime("%H:%M") for i in self.candidate_times]

        self.fig = make_subplots(
            rows=len(self.candidate_times), cols=1, subplot_titles=titles
        )

        for k, v in self.dictionaries.items():
            for trace_dict in v:
                self.fig.add_shape(**trace_dict, row=k + 1, col=1)

        for k, v in self.traces.items():
            for trace in v:
                self.fig.add_trace(trace, row=k + 1, col=1)

        self.fig["layout"]["showlegend"] = False  # type: ignore
        self.fig.add_trace(self.colorbar_trace)
        self.fig.update_layout(title_text=self.dataset_name)

        self.fig.show()

    def prepare_spatial_colors(self):
        min_val = min(self.spatial_values)
        max_val = max(self.spatial_values)
        for zone in self.plotter.zone_list:
            time_datas = zone.extracted_data[self.dataset_name]
            for ix, data in enumerate(time_datas):
                val = data.value
                norm_val = min_max_norm(val, min_val, max_val)
                color = get_norm_plotly_colors(
                    norm_val, min_val, max_val, color_scheme=self.color_scheme  # type: ignore
                )[0]
                zone.color_extracted_data(self.dataset_name, ix, color)

        self.colorbar_trace = create_colorbar(
            min_val, max_val, color_scheme=self.color_scheme  # type: ignore
        )

    def prepare_spatial_plots(self):
        self.dictionaries = {}
        self.traces = {}

        for ix, time in enumerate(self.candidate_times):
            self.dictionaries[ix] = []
            self.traces[ix] = []
            for zone in self.plotter.zone_list:
                data = zone.extracted_data[self.dataset_name][ix]
                trace_dict = prepare_shape_dict(
                    zone.polygon,
                    color=data.color,
                    # TODO edit for units..
                    label=f"{zone.display_name}: {data.value}ºC",
                )
                self.dictionaries[ix].append(trace_dict)

                for wall in zone.wall_list:
                    trace = prepare_line_traces(
                        wall.line, color="black", label=f"Wall {wall.number}"
                    )
                    self.traces[ix].append(trace)

    def check_dataset_is_zonal(self):
        if "zone" not in self.dataset_name:
            raise Exception(f"Dataset `{self.dataset_name}` is not zonal!")
