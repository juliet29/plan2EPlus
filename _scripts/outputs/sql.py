import os
from munch import Munch
from ladybug.sql import SQLiteResult

from outputs.input_classes import SQLInputs
from outputs.variables import OutputVars

class SQLReader:

    def __init__(self, inputs: SQLInputs) -> None:
        self.inputs = inputs
        self.analysis_period = None
        self.get_sql_results()

    def get_sql_results(self):
        try:
            SQL_PATH = os.path.join(self.inputs.path, "results", "eplusout.sql")
            self.sqld = SQLiteResult(SQL_PATH)
        except:
            raise Exception("7/30 SQL modification failed..")
        

    def get_collection_for_variable(self, output_var:OutputVars):
        self.curr_output = output_var
        self.validate_request()
        self.collection = self.sqld.data_collections_by_output_name(
            self.curr_output.value
        )
        self.split_collection_by_ap()

    def validate_request(self):
        assert self.curr_output.value in self.sqld.available_outputs, f"{self.curr_output.value} not in {self.sqld.available_outputs}"  # type: ignore

    def split_collection_by_ap(self):
        self.collection_by_ap = Munch()
        for dataset in self.collection:
            # TODO maybe use a shorter name..
            ap = str(dataset.header.analysis_period)
            if ap not in self.collection_by_ap.keys():
                self.collection_by_ap.update({ap: []})
            self.collection_by_ap[ap].append(dataset)

    def filter_collections(self):
        if self.analysis_period == None:
            self.set_analysis_period()
        self.filtered_collection = self.collection_by_ap[self.analysis_period]
        self.get_collection_geometry_type(self.filtered_collection[0])

    
    def set_analysis_period(self, ix=0):
        # TODO issue => what if dont have a collection yet.. actually no bc will have called the stuff above.. 
        possible_ap = list(self.collection_by_ap.keys())
        assert possible_ap, "No analysis periods"
        self.analysis_period = possible_ap[ix]


    def show_analysis_periods(self):
        for ix, k in enumerate(self.collection_by_ap.keys()):
            print(f"{ix} - {k}")

    def get_var_data(self, var:OutputVars):
        self.get_collection_for_variable(var)
        self.filter_collections()
        return self.filtered_collection

    def get_collection_geometry_type(self, dataset):
        metadata = dataset.header.metadata
        types = ["System", "Zone", "Surface"]

        for curr_type in types:
            try:
                metadata[curr_type]
                self.geom_type = curr_type
                return
            except:
                pass
        raise Exception(f"didnt find type {curr_type}")