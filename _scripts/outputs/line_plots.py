
from outputs.helpers import create_plot_title
from outputs.input_classes import LinePlotInputs
import plotly.graph_objects as go

from helpers.idf_object_rename import zone_rename


class LinePlot:
    def __init__(self, inputs:LinePlotInputs) -> None:
        self.inputs = inputs
        

    def create_plot(self):
        self.fig = go.Figure()

        title = None
        for dataset in self.inputs.collection_by_ap:
            shorter_name = self.shorten_name(dataset.header.metadata[self.inputs.geom_type])
            self.fig.add_trace(go.Scatter(
            x=dataset.datetimes, y=dataset.values, 
            name=shorter_name))

            if not title:
                title = create_plot_title(dataset)
                self.fig.update_layout(title_text=title)

        return self.fig
    
    def shorten_name(self, name):
        try:
            _, _, bunch_name = zone_rename(name)
            return bunch_name
        except: 
            return name 
    


            