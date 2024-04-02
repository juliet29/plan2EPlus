from geomeppy import IDF
import sys
import os
from icecream import ic

ENERGY_PLUS_LOCATION = "../../../../../Applications/EnergyPlus-22-2-0"
IDD_FILE = f"{ENERGY_PLUS_LOCATION}/Energy+.idd"
IDF_FILE = f"{ENERGY_PLUS_LOCATION}/ExampleFiles/Minimal.idf"

WEATHER_FILE = "weather/CA_PALO-ALTO-AP_724937S_20.epw"

IDF.setiddname(IDD_FILE)


def new_idf():
    idf = IDF(IDF_FILE)
    idf.epw = WEATHER_FILE

    return idf

def print_idf_in_file(idf:IDF, file="temp_idf"):
    sys.stdout = open(f'{file}.txt','wt')
    print(idf.idfstr())

    return

class EneryPlusCase:
    def __init__(self, case_name:str) -> None:
        # make case folder
        self.path = os.path.join("cases", case_name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        # initialize starting IDF File 
        self.idf = IDF(IDF_FILE)
        self.idf.epw = WEATHER_FILE

    def save_idf(self):
        # TODO what if there are multiple saves (and runs..)
        self.idf.save(filename=os.path.join(self.path, "out.idf"))

    def create_obj(self):
        self.idf.to_obj(fname=os.path.join(self.path, "out.obj"))

    def run_idf(self):
        self.idf.run(output_directory=os.path.join(self.path, "results"))


