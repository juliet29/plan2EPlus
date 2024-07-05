
from outputs.helpers import create_plot_title
from outputs.input_classes import PlotInputs
import plotly.graph_objects as go


class LinePlot:
    def __init__(self, inputs:PlotInputs) -> None:
        self.inputs = inputs
        

    def create_plot(self):
        self.fig = go.Figure()

        title = None
        for dataset in self.inputs.collection_by_ap:
            self.fig.add_trace(go.Scatter(
            x=dataset.datetimes, y=dataset.values, 
            name=dataset.header.metadata[self.inputs.geom_type]))

            if not title:
                title = create_plot_title(dataset)
                self.fig.update_layout(title_text=title)

        return self.fig

            