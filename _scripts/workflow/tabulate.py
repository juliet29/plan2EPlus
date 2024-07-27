import os
import pickle
import pandas as pd

from outputs.variables import OutputVars
from outputs.sql import SQLReader
from outputs.input_classes import SQLInputs


class Tabulate:
    def __init__(self, project_name) -> None:
        self.project_name = project_name

    def run(self):
        self.prepare_cases()
        self.create_tabular_data()


    def prepare_cases(self):
        self.project_path = os.path.join("cases", "projects", self.project_name)


        case_names = [f.name for f in os.scandir(self.project_path) if f.is_dir()]
        case_names.sort()
        self.data = {case: {} for case in case_names}


    def create_tabular_data(self):
        for case in self.data.keys():
            path = os.path.join(self.project_path, case, "input.pkl") 
            self.get_case_sql(path)
            # TODO make this work for various values of interest => should also have seperate dictionary that has the units.. 
            self.data[case].update({"peak_temp": self.get_peak_temperature()})
        self.df = pd.DataFrame.from_dict(self.data)
        self.df.to_csv(os.path.join(self.project_path, "output.csv"))


    def get_case_sql(self, case_path):
        with open(case_path, "rb") as handle:
            ez_input = pickle.load(handle)

        sql_input = SQLInputs(
            ez_input.case_name,
            ez_input.geometry,
            ez_input.output_variables,
            ez_input.project_name,
        )
        self.sql = SQLReader(sql_input)


    # TODO move .. 
    def get_peak_temperature(self):
        self.sql.get_collection_for_variable(OutputVars.zone_mean_air_temp)
        self.sql.filter_collections()
        value = max([i.max for i in self.sql.filtered_collection])
        return value

    
