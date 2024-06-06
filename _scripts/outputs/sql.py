import os
from enum import Enum
from icecream import ic

from ladybug.sql import SQLiteResult
from ladybug.analysisperiod import AnalysisPeriod

from case_edits.epcase import EneryPlusCaseReader
from geometry.geometry_parser import GeometryParser

from outputs.variables import OutputVars
from outputs.classes import GeometryOutputData



def create_analysis_period(ap_dict):
    ap_dict.pop("type")
    ap = AnalysisPeriod(**ap_dict)
    ap_name = f"{ap.st_month}-{ap.st_day}"
    return ap, ap_name

class GeomType(Enum):
    Zone = 0
    Surface = 1

class SQLReader:
    def __init__(self, CASE_NAME) -> None:
        self.case_name = CASE_NAME
        self._get_sql_outputs()
        self._get_geometry()

        self.curr_output = None
        self.requested_outputs = []

        self.dataset_names = []


        

    def _get_sql_outputs(
        self,
    ):
        SQL_PATH = os.path.join("cases", self.case_name, "results", "eplusout.sql")
        self.sqld = SQLiteResult(SQL_PATH)

    def _get_geometry(self):
        self.epcase = EneryPlusCaseReader(self.case_name)
        self.geo = GeometryParser(self.epcase.idf)
        self.geo.get_zones()
        self.create_zone_data_structure()
        self.create_wall_data_structure()
        
    def create_zone_data_structure(self):
        self.zone_list = self.geo.zones
        self.zone_dict = {i.name.upper(): i for i in self.geo.zones}

    def create_wall_data_structure(self):
        self.wall_dict = {}
        for zone in self.zone_list:
            for wall in zone.walls:
                self.wall_dict[wall.name.upper()] = wall
         

    def request_output(self, output_var:OutputVars):
        self.curr_output = output_var
        self.validate_request()
        self.update_requested_outputs()

        if GeomType.Zone.name in self.curr_output.value:
            self.geom_type = GeomType.Zone.name
            self.data_structure = self.zone_dict

        elif GeomType.Surface.name in self.curr_output.value:
            self.geom_type = GeomType.Surface.name
            self.data_structure = self.wall_dict
            
        self._match_geom_sql()
         

    def _match_geom_sql(self):
        collection = self.sqld.data_collections_by_output_name(self.curr_output.value)

        for dataset in collection:
            self.header = dataset.header.to_dict()
            self.geom_name = self.header["metadata"][self.geom_type]

            if "ROOF" in self.geom_name:
                continue

            self.create_output_object(dataset)

            self.handle_match_geom()


    def create_output_object(self, dataset):
        ap, ap_name = create_analysis_period(
                self.header["analysis_period"]
            )
        dataset_name = f"{self.curr_output.name}{ap_name}"
        self.update_dataset_names(dataset_name)
        self.output_object = GeometryOutputData(dataset, ap, dataset_name)


    def handle_match_geom(self):
        try:
            self.data_structure[self.geom_name].create_output_data(self.output_object)
        except:
            print(f"No match in data structure for {self.geom_name}, trying to fit.. ")
            key = self.find_matching_key()
            if key:
                print("success!")
                self.data_structure[key].create_output_data(self.output_object)
            else:
                raise Exception("Stil no match")


    def find_matching_key(self):
        for key in self.data_structure.keys():
            if key in self.geom_name:
                return key
            
    
    def validate_request(self):
        assert self.curr_output.value in self.sqld.available_outputs, f"{self.curr_output.value} not in {self.sqld.available_outputs}"


    def update_dataset_names(self, dataset_name):
        if dataset_name not in self.dataset_names:
                        self.dataset_names.append(dataset_name)

    def update_requested_outputs(self):
        self.requested_outputs.append(self.curr_output)
