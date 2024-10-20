from __future__ import annotations

import os
import filecmp

from icecream import ic 

# import geometry.geometry_parser as geom
from geomeppy import IDF
from ladybug.epw import EPW
from eppy.runner.run_functions import EnergyPlusRunError

from case_edits.defaults import IDF_PATH, IDD_PATH, WEATHER_FILE


IDF.setiddname(IDD_PATH) # TODO this may be a problem later.. 



class EneryPlusCaseEditor:
    def __init__(self, case_name:str, starting_case:str="", project_name="",) -> None: # type: ignore
        self.project_name = project_name
        self.starting_case = starting_case
        self.case_name = case_name
        self.is_changed_idf = True
        self.is_failed_simulation = False
        
        self.make_case_folder()
        self.get_idf()
        self.update_weather_and_run_period()

        
    def __repr__(self):
        return f"EPCaseEditor({self.case_name})"  
    
    def make_case_folder(self):
        if self.project_name:
            self.path = os.path.join("cases", "projects", self.project_name, self.case_name)
        else:
            self.path = os.path.join("cases", self.case_name)
            
        if not os.path.exists(self.path):
            os.makedirs(self.path)


    def get_idf(self):
        if not self.starting_case:
            self.idf = IDF(IDF_PATH) 
        else:
            self.starting_idf_path = os.path.join("cases", self.starting_case, "out.idf")
            self.idf = IDF(self.starting_idf_path)  


    def compare_and_save(self):
        self.temp_idf_path = os.path.join(self.path, "temp.idf")
        self.idf_path = os.path.join(self.path, "out.idf")
        self.idf.save(filename=self.temp_idf_path)

        curr_case_files = next(os.walk(self.path))[2]
        if "out.idf" in curr_case_files:
            print("out.idf exists")
            self.is_changed_idf = not filecmp.cmp(self.temp_idf_path, self.idf_path)
            print(f"IDF has changed: {self.is_changed_idf}")
        else:
            print("out.idf does not exist")
            self.is_changed_idf = True
            # TODO based on results.. 

        self.idf.save(filename=self.idf_path)
        os.remove(self.temp_idf_path)

        
    def run_idf(self, force_run = False):
        if self.is_changed_idf or force_run:
            print("idf has changed - running case")
            try:
                self.idf.run(output_directory=os.path.join(self.path, "results"))
            except EnergyPlusRunError:
                self.is_failed_simulation = True
                print(f"Simulation for case `{self.case_name}` failed - see error logs")
                err_file = os.path.join(self.path, "results", "eplusout.err")
                print(err_file)

            # self.is_changed_idf = False
        else:
            print("idf has not changed - no run")


    # def get_geometry(self):
    #     self.geometry = geom.GeometryParser(self.idf) 


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


class EneryPlusCaseReader:
    def __init__(self, case_name:str) -> None:
        IDF_PATH = os.path.join("cases", case_name, "out.idf")
        self.idf = IDF(IDF_PATH)
        self.case_name = case_name
        
        # self.get_geometry()

    def __repr__(self):
        return f"EPCaseReader({self.case_name})"  

    # def get_geometry(self):
    #     self.geometry = geom.GeometryParser(self.idf)  