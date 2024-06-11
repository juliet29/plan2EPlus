import os
from geomeppy import IDF
from geometry.geometry_parser import GeometryParser

from case_edits.defaults import IDF_PATH, IDD_PATH, WEATHER_FILE


IDF.setiddname(IDD_PATH) # TODO this may be a problem later.. 


class EneryPlusCaseReader:
    def __init__(self, case_name:str) -> None:
        IDF_PATH = os.path.join("cases", case_name, "out.idf")
        self.idf = IDF(IDF_PATH)
        self.case_name = case_name
        self.get_geometry()

    def __repr__(self):
        return f"EPCaseReader({self.case_name})"  

    def get_geometry(self):
        self.geometry = GeometryParser(self.idf)  


class EneryPlusCaseEditor:
    # TODO make this inherit the other? to the extent it cane?
    def __init__(self, case_name:str, starting_case:str=None) -> None:
        # make case folder
        self.path = os.path.join("cases", case_name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # initialize starting IDF File
        self.starting_case = starting_case
        self.get_idf()
        self.idf.epw = WEATHER_FILE #TODO this isnt working bc still denver.. 

        self.case_name = case_name

    def __repr__(self):
        return f"EPCaseEditor({self.case_name})"  

    def get_idf(self):
        if not self.starting_case:
            self.idf = IDF(IDF_PATH)
        else:
            self.starting_idf_path = os.path.join("cases", self.starting_case, "out.idf")
            self.idf = IDF(self.starting_idf_path)  

    def get_geometry(self):
        self.geometry = GeometryParser(self.idf)  

    def save_idf(self):
        # TODO what if there are multiple saves (and runs..) => check if want to overwrite existing file.. 
        self.idf.save(filename=os.path.join(self.path, "out.idf"))

    def create_obj(self):
        # this is for 3d objects!
        self.idf.to_obj(fname=os.path.join(self.path, "out.obj"))


    def prepare_to_run(self):
        self.idf.intersect_match()
        self.idf.set_default_constructions()
        # self.save_idf()

    def run_idf(self, run_local=False):
        # TODO not sure why this is here.. 
        # TODO check if overwriting existing files and ask if want to proceed...
        if not run_local:
            self.idf.run(output_directory=os.path.join(self.path, "results"))
        else:
            self.idf.run(
                idf=os.path.join(self.path, "out.idf"),
                output_directory=os.path.join(self.path, "results"),
            )
