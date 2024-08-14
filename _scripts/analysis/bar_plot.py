from typing import List
from enum import Enum

import numpy as np
import pandas as pd
import plotly.express as px

from ladybug.dt import Time

from case_edits.ezcase import EzCase
from outputs.variables import OutputVars as ov

class PlotType(Enum):
    STACKED_BAR = 0
    VIOLIN = 1




# TODO, will need a custom input, not the whole ezcase.. 
class BarPlotAnalysis:
    def __init__(self, ez:EzCase, qois:List[ov], plot_type:int=0, time:tuple=(12,0), qoi_names=[]) -> None:
        assert ez.plt
        assert ez.case

        self.plt = ez.plt
        self.zone_list = ez.case.geometry.zone_list
        self.case_name = ez.case.case_name

        self.qois = qois
        self.time = time

        self.plot_type = PlotType(plot_type)

        self.long_data = []

        self.qoi_names = qoi_names


    def run(self):
        for ix, qoi in enumerate(self.qois):
            self.qoi = qoi
            self.qoi_name = self.qoi_names[ix] if self.qoi_names else self.qoi.name
            self.get_data()
            if ix == 0:
                self.get_time_index()

            for zone in self.zone_list:
                self.curr_zone = zone
                self.get_zone_values()

                if self.plot_type == PlotType.STACKED_BAR:
                    self.get_value_at_time()
                    self.create_single_value_entry()
                elif self.plot_type == PlotType.VIOLIN:
                    self.create_many_value_entry()


        self.df = pd.DataFrame(self.long_data)

    
    def get_data(self):
        self.plt.get_collection_for_variable(self.qoi)
        self.plt.filter_collections()
        self.curr_collection = self.plt.filtered_collection
    
    def get_time_index(self):
        assert self.curr_collection
        datetimes = list(self.curr_collection[0].datetimes)
        f = filter(lambda x: x.time == Time(*self.time), datetimes)
        self.time_ix = datetimes.index(next(f))

    def get_zone_values(self):
        surf_values = []
        for surface in self.curr_collection:
            if self.curr_zone.name.upper() in surface.header.metadata["Surface"]:
                surf_values.append(np.array(surface.values))

        # NOTE: aggregating by summing, assuming rate/area is qoi
        # TODO use numpy to reduce.. 
        self.zone_values = sum(surf_values)
        return self.zone_values
        
        

    def get_value_at_time(self):
        self.block_val_at_time = self.zone_values[self.time_ix] # type:ignore 


    def create_single_value_entry(self):
        d = {
            "room": self.curr_zone.bunch_name,
            "qoi": self.qoi.name,
            "value": self.block_val_at_time
        }
        self.long_data.append(d)


    def create_many_value_entry(self):
        for time, value in zip(self.curr_collection[0].datetimes, self.zone_values): #type:ignore
            d = {
                "room": self.curr_zone.bunch_name,
                "qoi": self.qoi_name,
                "time": time,
                "value": value
            }
            self.long_data.append(d)


    def create_stacked_bar_plot(self):
        self.fig = px.bar(self.df, x="room", y="value", color="qoi", title=f"{self.case_name} at {self.time}")
        self.fig.show()




