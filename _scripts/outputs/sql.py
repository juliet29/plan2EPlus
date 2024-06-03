import os
from ladybug.sql import SQLiteResult
from ladybug.analysisperiod import AnalysisPeriod

from helpers.helpers import min_max_norm
from helpers.plots import get_norm_plotly_colors, create_colorbar

from case_edits.epcase import EneryPlusCaseReader
from geometry.geometry_parser import GeometryParser

from outputs.output_names import OutputVariables
from outputs.output_data import OutputData, GeometryOutputData, TimeExtractData


def create_analysis_period(ap_dict):
    ap_dict.pop("type")
    ap = AnalysisPeriod(**ap_dict)
    ap_name = f"{ap.st_month}-{ap.st_day}"
    return ap, ap_name


class SQLReader:
    def __init__(self, CASE_NAME) -> None:
        self.case_name = CASE_NAME
        self.get_sql_outputs()
        self.get_geometry()


        self.dataset_names = []

    def get_sql_outputs(self, ):
        SQL_PATH = os.path.join("cases", self.case_name, "results","eplusout.sql" )
        self.sqld = SQLiteResult(SQL_PATH)


    def get_geometry(self):
        e = EneryPlusCaseReader(self.case_name)
        geo = GeometryParser(e.idf)
        geo.get_zones()
        self.zone_dict =  {i.name.upper(): i  for i in geo.zones}
        
    def match_geom_sql(self, output_var=OutputVariables.zone_mean_air_temp):
        self.collection = self.sqld.data_collections_by_output_name(output_var.value)

        for dataset in self.collection:
            ap, ap_name = create_analysis_period(dataset.header.to_dict()["analysis_period"])
            dataset_name = f"{output_var.name}{ap_name}"
            out_data = GeometryOutputData(dataset, ap, dataset_name)

            zone_name = dataset.header.to_dict()["metadata"]["Zone"] 
            self.zone_dict[zone_name].create_output_data(out_data)

            if dataset_name not in self.dataset_names:
                self.dataset_names.append(dataset_name)

    # to own function if want to think about different times.. 

    def extract_time_data(self, time_index, dataset_name):
        self.spatial_values = []
        for zone in self.zone_dict.values():
            value = zone.output_data[dataset_name].dataset.values[time_index]
            self.spatial_values.append(value)
            data = TimeExtractData(value)
            zone.create_extracted_data(dataset_name, data)
            

    def prepare_spatial_colors(self, dataset_name):
        min_val = min(self.spatial_values)
        max_val = max(self.spatial_values)
        for zone in self.zone_dict.values():
            val = zone.extracted_data[dataset_name].value
            norm_val = min_max_norm(val, min_val, max_val)
            color = get_norm_plotly_colors(norm_val, min_val, max_val)[0]
            zone.color_extracted_data(dataset_name, color)

        self.colorbar_trace = create_colorbar(min_val, max_val)

    # def prepare_colorbar(self):
    #     pass






    # def get_zone_level_data(self, index):
    #     # TODO assert that this data is at the zone level 
    #     self.collection = self.sqld.data_collections_by_output_name(OutputVariables.zone_mean_air_temp.value)

    #     zone_name = self.collection[index].header.to_dict()["metadata"]["Zone"]
    #     times = self.collection[index].datetimes
    #     values = self.collection[index].values 
    #     self.data[index] = OutputData(zone_name, times, values)



    # def prepare_spatial_data(self, time_indices):
    #     # TODO => map times to indices ..

    #     self.spatial_data = {}
    #     self.spatial_times = []
    #     self.spatial_values = []
    #     for time_ix in time_indices:
    #         self.spatial_data[time_ix] = []
    #         for ix, val in enumerate(self.data.values()):
    #             value = round(val.values[time_ix],3)
    #             self.spatial_data[time_ix].append([val.name, value])
    #             self.spatial_values.append(value)
    #             if ix == 0:
    #                 self.spatial_times.append(val.times[time_ix])


        


            



        

        

