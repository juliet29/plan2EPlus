import plotly.graph_objects as go

from outputs.sql import SQLReader

class TimePlot(SQLReader):
    def __init__(self, CASE_NAME) -> None:
        super().__init__(CASE_NAME)


    def make_time_plot(self, dataset_name):
        self.fig = go.Figure()

        for zone in self.zone_list:
            dataset = zone.output_data[dataset_name].dataset
            self.fig.add_trace(go.Scatter(x=dataset.datetimes, y=dataset.values, name=zone.name))

        self.fig.update_layout(title_text=dataset_name)

        self.fig.show()
