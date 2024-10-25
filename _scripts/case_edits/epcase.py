

import os
import filecmp
from pathlib import Path
from typing import Optional
from geomeppy import IDF
from ladybug.epw import EPW
from eppy.runner.run_functions import EnergyPlusRunError

from case_edits.defaults import IDF_PATH, IDD_PATH, WEATHER_FILE


IDF.setiddname(IDD_PATH)



class EneryPlusCaseEditor:
    def __init__(self, path_to_outputs:Path, starting_path:Optional[Path]=None) -> None: 
        self.path = path_to_outputs
        self.case_name = self.path.name
        self.starting_path = starting_path
        self.is_changed_idf = True
        self.is_failed_simulation = False
        
        self.get_idf()
        self.update_weather_and_run_period()

        
    def __repr__(self):
        return f"EPCaseEditor({self.case_name})"  
    

    def get_idf(self):
        if not self.starting_path:
            self.idf = IDF(IDF_PATH) 
        else:
            self.idf = IDF(self.starting_path)  


    def compare_and_save(self):
        self.temp_idf_path = self.path / "temp.idf"
        self.idf_path = self.path / "out.idf"
        self.idf.save(filename=self.temp_idf_path)

        dir_files = list(self.path.iterdir())
        if "out.idf" in dir_files:
            print("out.idf exists")
            self.is_changed_idf = not filecmp.cmp(self.temp_idf_path, self.idf_path)
            print(f"IDF has changed: {self.is_changed_idf}")
        else:
            print("out.idf does not exist")
            self.is_changed_idf = True

        self.idf.save(filename=self.idf_path)
        os.remove(self.temp_idf_path)

        
    def run_idf(self, force_run = False):
        if self.is_changed_idf or force_run:
            print("idf has changed - running case")
            try:
                self.idf.run(output_directory=os.path.join(self.path, "results"))
            except EnergyPlusRunError:
                self.is_failed_simulation = True
                print(f"Simulation for case `{self.path}` failed - see error logs")
    
        else:
            print("idf has not changed - no run")




    def update_weather_and_run_period(self):
        self.idf.epw = WEATHER_FILE
        epw = EPW(self.idf.epw)
        loc = self.idf.newidfobject("SITE:LOCATION")
        loc.Name = epw.location.city
        loc.Latitude = epw.location.latitude
        loc.Longitude = epw.location.longitude
        loc.Time_Zone = epw.location.time_zone
        loc.Elevation = epw.location.elevation

        ap1 = self.idf.newidfobject("RUNPERIOD")
        ap1.Name = "SummerDay"
        ap1.Begin_Month = 7
        ap1.Begin_Day_of_Month = 1
        ap1.End_Month = 7
        ap1.End_Day_of_Month = 1
