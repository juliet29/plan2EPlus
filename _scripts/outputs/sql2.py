from outputs.input_classes import SQLInputs, PlotInputs
import os
from ladybug.sql import SQLiteResult
from ladybug.analysisperiod import AnalysisPeriod
from munch import Munch
from outputs.line_plots import LinePlot

class SQLReader:
    def __init__(self, inputs: SQLInputs) -> None:
        self.inputs = inputs
        self.get_sql_results()

    def get_sql_results(self):
        # TODO most of this path should come from EZCase or EPCase.. 
        SQL_PATH = os.path.join(
            "cases", self.inputs.case_name, "results", "eplusout.sql"
        )
        self.sqld = SQLiteResult(SQL_PATH)

    def get_collection_for_variable(self, output_var):
        self.curr_output = output_var
        self.validate_request()
        self.collection = self.sqld.data_collections_by_output_name(self.curr_output.value)
        self.split_collection_by_ap()

    def set_analysis_period(self, ix):
        possible_ap = list(self.collection_by_ap.keys())
        self.analysis_period = possible_ap[ix]


    def create_plot(self, plot_type="line"):
        assert self.analysis_period, "Call `set_analysis_period`"

        collection = self.collection_by_ap[self.analysis_period]
        self.get_collection_geometry_type(collection[0])
        if plot_type=="line":
            self.line_plot_obj = LinePlot(PlotInputs(collection, self.geom_type))
            self.line_plot_obj.create_plot()
            self.line_plot_obj.fig.show()


    def split_collection_by_ap(self):
        self.collection_by_ap = Munch()
        for dataset in self.collection:
            # TODO maybe use a shorter name.. 
            ap = str(dataset.header.analysis_period)
            if ap not in self.collection_by_ap.keys():
                self.collection_by_ap.update({ap: []})
            self.collection_by_ap[ap].append(dataset)
        # self.show_analysis_periods()

    def show_analysis_periods(self):
        for ix, k in enumerate(self.collection_by_ap.keys()):
            print(f"{ix} - {k}")
        
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
    


    def validate_request(self):
        assert (self.curr_output.value in self.sqld.available_outputs), f"{self.curr_output.value} not in {self.sqld.available_outputs}"  # type: ignore
