import os
from ladybug.sql import SQLiteResult
from ladybug.analysisperiod import AnalysisPeriod

from helpers.helpers import min_max_norm
from helpers.plots import get_norm_plotly_colors

from case_edits.epcase import EneryPlusCaseReader
from geometry.geometry_parser import GeometryParser

from outputs.output_names import OutputVariables
from outputs.output_data import OutputData, GeometryOutputData


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


        self.data = {}

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
            zone_name = dataset.header.to_dict()["metadata"]["Zone"] 
            ap, ap_name = create_analysis_period(dataset.header.to_dict()["analysis_period"])
            dataset_name = f"{output_var.name}{ap_name}"
            out_data = GeometryOutputData(dataset, ap, dataset_name)
            
            self.zone_dict[zone_name].update_output_data(out_data)






    def get_zone_level_data(self, index):
        # TODO assert that this data is at the zone level 
        self.collection = self.sqld.data_collections_by_output_name(OutputVariables.zone_mean_air_temp.value)

        zone_name = self.collection[index].header.to_dict()["metadata"]["Zone"]
        times = self.collection[index].datetimes
        values = self.collection[index].values 
        self.data[index] = OutputData(zone_name, times, values)

        # TODO use are_collections_aligned(data_collections, raise_exception=True) to check => only want to look at data for one analysis period ..

    def prepare_spatial_data(self, time_indices):
        # TODO => map times to indices ..

        self.spatial_data = {}
        self.spatial_times = []
        self.spatial_values = []
        for time_ix in time_indices:
            self.spatial_data[time_ix] = []
            for ix, val in enumerate(self.data.values()):
                value = round(val.values[time_ix],3)
                self.spatial_data[time_ix].append([val.name, value])
                self.spatial_values.append(value)
                if ix == 0:
                    self.spatial_times.append(val.times[time_ix])

    def prepare_spatial_colors(self):
        min_val = min(self.spatial_values)
        max_val = max(self.spatial_values)
        for time in self.spatial_data.values():
            for zone in time:
                #TODO turn into class?
                norm_val = min_max_norm(zone[1], min_val, max_val)
                color = get_norm_plotly_colors(norm_val, min_val, max_val)[0]
                zone.append(color)

        


            



        

        

