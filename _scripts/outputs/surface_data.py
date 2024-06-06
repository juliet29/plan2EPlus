from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helpers.plots import get_plotly_colors
from geometry.wall import CardinalDirection
from outputs.sql import SQLReader

class SurfaceData(SQLReader):
    def __init__(self, CASE_NAME) -> None:
        super().__init__(CASE_NAME)


    def prepare_titles(self):
        self.direction_names = [CardinalDirection(i).name for i in [0,90,180,270]]
        self.direction_titles = [f"{i.title()} Walls" for i in self.direction_names]

    def create_color_map(self):
        # TODO update for more zones.. 
        # colors, _ = get_plotly_colors(n_colors=2)

        colors = ["blue", "red"]
        assert len(colors) == len(self.zone_list)
        self.color_map = {zone.short_name:color for zone, color in zip(self.zone_list, colors)}


    def create_fig(self, dataset_name):
        # TODO check that correct kind of dataset! 

        self.prepare_titles()
        self.create_color_map()

        fig = make_subplots(rows=len(self.direction_names), cols=1, subplot_titles=self.direction_titles, shared_xaxes=True)

        for ix, direction in enumerate(self.direction_names):
            row = ix+1
            for wall in self.wall_list:
                if wall.direction == direction:
                    try:
                        data = wall.output_data[dataset_name]
                    except:
                        print(f"No data for {wall.name2}")
                        continue
                    dataset = data.dataset

                    color = self.color_map[wall.zone]
                    fig.add_trace(go.Scatter(x=dataset.datetimes, y=dataset.values, legendgroup=wall.zone, name=f"{wall.zone} Block", line=dict(color=color)), row=row, col=1)


            fig.update_layout(
                    title_text=f"{data.analysis_period_name} {data.formal_name} [{data.unit}]",
                )

        return fig
