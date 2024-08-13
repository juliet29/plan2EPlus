from typing import List

import numpy as np
import pandas as pd
from ladybug.dt import Time

from case_edits.ezcase import EzCase
from outputs.variables import OutputVars as ov


# TODO, will need a custom input, not the whole ezcase.. 
class BarPlotAnalysis:
    def __init__(self, ez:EzCase, qois:List[ov], time:tuple=(12,0)) -> None:
        assert ez.plt
        assert ez.case

        self.plt = ez.plt

        self.zone_list = ez.case.geometry.zone_list
        self.qois = qois
        self.qoi = self.qois[0]

        self.time = time

        self.long_data = []


    def run(self):
        for ix, qoi in enumerate(self.qois):
            self.qoi = qoi
            self.get_data()
            if ix == 0:
                self.get_time_index()

            for zone in self.zone_list:
                self.curr_zone = zone
                self.get_zone_values()
                self.get_value_at_time()
                self.create_entry()
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
        self.zone_values = sum(surf_values)
        

    def get_value_at_time(self):
        self.block_val_at_time = self.zone_values[self.time_ix] # type:ignore 


    def create_entry(self):
        d = {
            "room": self.curr_zone.bunch_name,
            "qoi": self.qoi.name,
            "value": self.block_val_at_time
        }
        self.long_data.append(d)


