import os
import pickle
import pandas as pd
from typing import Union, Optional
from warnings import warn

import seaborn as sns
import seaborn.objects as so

from outputs.variables import OutputVars, PostProcessedOutputVars
from outputs.sql import SQLReader
from outputs.input_classes import SQLInputs

from helpers.idf_object_rename import zone_rename




sns.set_theme(rc={"figure.figsize": (5.5, 4)})
VariableType = Optional[Union[OutputVars, PostProcessedOutputVars]]


class BiVariableAnalysis:
    def __init__(self, project_name) -> None:
        self.project_name = project_name
        self.case_sqls = {}
        self.case_ppd = {}
        self.qoi1 = None
        self.qoi2 = None
        self.is_post_processed_qois = (False, False)
        self.is_zonal_data = True
        self.is_two_by_two = False

    def update_qois(self, qoi1: VariableType = None, qoi2: VariableType = None):
        # qoi1 is the indpendent variable ~ site wind speed
        if qoi1:
            self.qoi1 = qoi1
        if qoi2:
            self.qoi2 = qoi2

    def update_is_post_process_qoi(
        self, qoi1_bool: bool = False, qoi2_bool: bool = False
    ):
        self.is_post_processed_qois = (qoi1_bool, qoi2_bool)

    def run(self):
        if not self.case_sqls:
            self.prepare_cases()
            self.get_case_sqls()
            self.get_case_post_processed_data()
        self.create_long_data()
        self.make_bivariable_plot()
        # self.create_tabular_data()

    def prepare_cases(self):
        self.project_path = os.path.join("cases", "projects", self.project_name)
        self.case_names = [f.name for f in os.scandir(self.project_path) if f.is_dir()]
        self.case_names.sort()

    def get_case_sqls(self):
        for case in self.case_names:
            path = os.path.join(self.project_path, case)
            sql = self.get_case_sql(path)
            self.case_sqls[case] = sql

    def get_case_post_processed_data(self):
        for case in self.case_names:
            path = os.path.join(self.project_path, case, "post_process.pkl")
            with open(path, "rb") as handle:
                self.case_ppd[case] = pickle.load(handle)

    def create_long_data(self):
        self.long_data = []
        for case in self.case_names:
            self.curr_case = case
            if self.pull_data():
                self.long_data.extend(self.get_zone_data(0))
                if self.is_zonal_data:
                    assert type(self.var2) == list
                    for zone_ix, _ in enumerate(self.var2):
                        if zone_ix==0:
                            pass
                        self.long_data.extend(self.get_zone_data(zone_ix))
        self.df = pd.DataFrame(self.long_data)

    def pull_data(self):
        if self.qoi1 and self.qoi2:
            self.sql = self.case_sqls[self.curr_case]
            self.ppd = self.case_ppd[self.curr_case]
            self.var1 = self.get_var_data(self.qoi1, self.is_post_processed_qois[0])
            self.var2 = self.get_var_data(self.qoi2, self.is_post_processed_qois[1])
            if type(self.var1) == list and type(self.var2) == list:
                if not self.is_two_by_two:
                    assert len(self.var1) == 1, f"{self.qoi1} is not a site var"
                return True
        else:
            raise Exception(f"Invalide QOIs:{self.qoi1}, {self.qoi2}")

    def get_var_data(self, var: VariableType, POST_PROCESS_DATA=False):
        try:
            if POST_PROCESS_DATA:
                return self.ppd[var]
            else:
                self.sql.get_collection_for_variable(var)
                self.sql.filter_collections()
                return self.sql.filtered_collection
        except:
            warn(
                f"Unable to pull data of {var} for {self.curr_case}"
            )
            return False

    def get_zone_data(self, ix):
        assert self.qoi1 and self.qoi2
        assert type(self.var1)== list and type(self.var2)== list
        try:
            _, _, zone_name = zone_rename(self.var2[ix].header.metadata["System"])
        except:
            _, _, zone_name = zone_rename(self.var2[ix].header.metadata["Zone"])




        var1_ix = ix if self.is_two_by_two else 0
        return [
            {
                "case": self.curr_case,
                "zone": zone_name,
                self.qoi1.name: v1,
                self.qoi2.name: v2,
            }
            
            for v1, v2 in zip(self.var1[var1_ix].values, self.var2[ix].values)
        ]

    def get_case_sql(self, case_path):
        input_path = os.path.join(case_path, "input.pkl")
        with open(input_path, "rb") as handle:
            ez_input = pickle.load(handle)

        sql_input = SQLInputs(
            case_name=ez_input.case_name,
            path=case_path,
            geometry=ez_input.geometry,
            output_variables=ez_input.output_variables,
            project_name=ez_input.project_name,
        )
        return SQLReader(sql_input)

    def make_bivariable_plot(self):
        assert self.qoi1 and self.qoi2
        self.fig = (
            so.Plot(self.df, x=self.qoi1.name, y=self.qoi2.name, color="zone")
            .layout(size=(8, 6))
            .facet("case")
            .add(so.Dots())
            # .add(so.Line(), so.PolyFit())
            # .scale(color="flare")  # type: ignore
        );
        # return self.fig
