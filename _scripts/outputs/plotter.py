from outputs.sql import SQLReader, SQLInputs
from outputs.zone_space_time import SpaceTimePlot
from outputs.zone_time import TimePlot
from outputs.surface_data import SurfaceData
from datetime import time
from typing import List




class Plotter(SQLReader):
    def __init__(self, inputs: SQLInputs) -> None:
        super().__init__(inputs)


    def set_color_schemes(self, color_scheme):
        self.color_scheme = color_scheme

    def check_dataset_is_zonal(self, dataset_name):
        if "zone" not in dataset_name:
            raise Exception(f"Dataset `{dataset_name}` is not zonal!")

    def check_dataset_is_surface(self, dataset_name):
        if "surf" not in dataset_name:
            raise Exception(f"Dataset `{dataset_name}` is not for surfaces!")
        
    # types of plots..
    def plot_zone_over_time(self, dataset):
        s = TimePlot(self)
        return s.make_time_plot(dataset)

    def plot_zone_at_different_time_2d(self, dataset, times:List[time]):
        s = SpaceTimePlot(self)
        s.extract_many_times(times, dataset)
        return s.create_spatial_plots()

    def plot_surface_over_time(self, dataset):
        s = SurfaceData(self)
        return s.create_fig(dataset)
        # fig.show()
  


    def plot_site_data_over_time(self, dataset):
        pass
        

