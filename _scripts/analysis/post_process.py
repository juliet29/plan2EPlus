import os
from copy import deepcopy
import pickle

import numpy as np

from ladybug.datacollection import HourlyContinuousCollection

from outputs.sql import SQLReader
from outputs.variables import OutputVars


class PostProcesser:
    def __init__(self, sql: SQLReader, path: str) -> None:
        self.sql = sql
        self.path = path
        self.data = {}

    def calc_defaults(self):
        self.calc_signed_difference_of_qois(
            OutputVars.zone_vent_heat_loss,
            OutputVars.zone_vent_heat_gain,
            "Zone Ventilation Net Heat Loss",
        )
        self.save_data()

    def calc_signed_difference_of_qois(
        self, qoi1: OutputVars, qoi2: OutputVars, qoi_name
    ):
        var1 = self.sql.get_var_data(qoi1)
        var2 = self.sql.get_var_data(qoi2)

        new_header = deepcopy(var1[0].header)
        new_header.metadata["type"] = qoi_name

        new_var = []
        for v1, v2 in zip(var1, var2):
            np_val = np.array(v1.values) - np.array(v2.values)
            new_vals = tuple(np_val.tolist())
            new_var.append(HourlyContinuousCollection(new_header, new_vals))
        self.data[qoi_name] = new_var

    def save_data(self):
        filename = os.path.join(self.path, "post_process.pkl")
        with open(filename, "wb") as handle:
            pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)
