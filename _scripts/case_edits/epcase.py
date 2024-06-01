import os
from geomeppy import IDF

from case_edits.defaults import IDF_PATH, IDD_PATH, WEATHER_FILE


IDF.setiddname(IDD_PATH) # TODO this may be a problem later.. 


class EneryPlusCaseReader:
    def __init__(self, CASE_NAME: str) -> None:
        IDF_PATH = os.path.join("cases", CASE_NAME, "out.idf")
        self.idf = IDF(IDF_PATH)


class EneryPlusCaseEditor:
    def __init__(self, case_name: str) -> None:
        # make case folder
        self.path = os.path.join("cases", case_name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # initialize starting IDF File
        self.idf = IDF(IDF_PATH)
        self.idf.epw = WEATHER_FILE

    def save_idf(self):
        # TODO what if there are multiple saves (and runs..)
        self.idf.save(filename=os.path.join(self.path, "out.idf"))

    def create_obj(self):
        # this is for 3d objects!
        self.idf.to_obj(fname=os.path.join(self.path, "out.obj"))

    # TODO add materials, intersect and match surfaces..

    def prepare_to_run(self):
        self.idf.intersect_match()
        self.idf.set_default_constructions()
        # self.save_idf()

    def run_idf(self, run_local=False):
        if not run_local:
            self.idf.run(output_directory=os.path.join(self.path, "results"))
        else:
            self.idf.run(
                idf=os.path.join(self.path, "out.idf"),
                output_directory=os.path.join(self.path, "results"),
            )
