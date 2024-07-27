import os
import pickle
import pandas as pd

from outputs.variables import OutputVars
from outputs.sql import SQLReader
from outputs.input_classes import SQLInputs


class ACH:
    def __init__(self, project_name) -> None:
        self.project_name = project_name
        self.case_sqls = {}

    def run(self):
        self.prepare_cases()
        self.get_case_sqls()
        self.create_long_data()
        # self.create_tabular_data()


    def prepare_cases(self):
        self.project_path = os.path.join("cases", "projects", self.project_name)
        self.case_names = [f.name for f in os.scandir(self.project_path) if f.is_dir()]
        self.case_names.sort()
    
    def get_case_sqls(self):
        for case in self.case_names:
            path = os.path.join(self.project_path, case, "input.pkl") 
            sql = self.get_case_sql(path)
            self.case_sqls[case] = sql

    
    def create_long_data(self):
        self.long_data = []
        for case in self.case_names:
            self.curr_case = case
            self.update_data()
            self.long_data.extend(self.get_zone_data(0))
            self.long_data.extend(self.get_zone_data(1))
        self.df = pd.DataFrame(self.long_data)

    def update_data(self):
        sql = self.case_sqls[self.curr_case]
        self.ach = self.get_var_data(sql, OutputVars.zone_ach)
        self.wspeed = self.get_var_data(sql,OutputVars.site_wind_speed)

    def get_zone_data(self, ix):
        return [{"case": self.curr_case, "zone": str(ix), "wspeed":v, "ach": ach} for v, ach in zip(self.wspeed[0].values, self.ach[ix].values)]
    

    def get_var_data(self, sql, var):
        sql.get_collection_for_variable(var)
        sql.filter_collections()
        return sql.filtered_collection


    def get_case_sql(self, case_path):
        with open(case_path, "rb") as handle:
            ez_input = pickle.load(handle)

        sql_input = SQLInputs(
            ez_input.case_name,
            ez_input.geometry,
            ez_input.output_variables,
            ez_input.project_name,
        )
        return SQLReader(sql_input)






