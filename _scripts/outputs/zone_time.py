import plotly.graph_objects as go

from outputs.plotter import Plotter


class TimePlot:
    def __init__(self, PlotterObj: Plotter) -> None:
        self.plotter = PlotterObj

    def make_time_plot(self, dataset_name):
        self.dataset_name = dataset_name
        self.plotter.check_dataset_is_zonal(dataset_name)
        self.fig = go.Figure()

        for zone in self.plotter.zone_list:
            dataset = zone.output_data[dataset_name].dataset
            self.fig.add_trace(
                go.Scatter(
                    x=dataset.datetimes, y=dataset.values, name=zone.display_name
                )
            )

        self.fig.update_layout(title_text=dataset_name)

        self.fig.show()
