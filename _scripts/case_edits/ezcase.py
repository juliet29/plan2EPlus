from dataclasses import dataclass
from typing import List, Tuple, Union, Sequence
from munch import Munch

from gplan.room_class import GPLANRoomAccess
from gplan.convert import GPLANtoGeomeppy

from case_edits.epcase import EneryPlusCaseEditor
from case_edits.special_types import PairType, GeometryType
from case_edits.methods.subsurfaces.inputs import SubsurfaceInputs, SubsurfaceAttributes, SubsurfaceObjects
from case_edits.methods.subsurfaces.creator import SubsurfaceCreator
from case_edits.methods.airflownetwork import AirflowNetwork
from case_edits.methods.outputs import OutputRequests

from outputs.variables import OutputVars as OV
from outputs.input_classes import SQLInputs, PlotterInputs
from outputs.sql import SQLReader
from outputs.plotter import Plotter
from outputs.base_2d import Base2DPlot

from pprint import pprint



@dataclass
class EzCaseInput:
    case_name:str
    door_pairs: Sequence[PairType]
    window_pairs: Sequence[PairType]
    output_variables:List[OV]
    geometry:GeometryType = GPLANRoomAccess("",0)
    starting_case:str=""

class EzCase():
    def __init__(self, input:EzCaseInput, RUN_CASE=False) -> None:
        self.inputs = input
        self.case = EneryPlusCaseEditor(self.inputs.case_name, self.inputs.starting_case)
        self.RUN_CASE = RUN_CASE
        self.run()

    def run(self):
        self.add_rooms()
        self.get_subsurface_constructions()
        self.get_geometry()
        self.update_geometry_walls()
        self.add_doors()
        self.add_windows()
        self.update_geometry_subsurfaces()
        self.add_airflownetwork()
        self.add_output_variables()
        self.case.save_idf()
        if self.RUN_CASE:
            self.case.run_idf()
        self.make_base_plot()
        self.prepare_plotter()


    def add_rooms(self):
        self.gplan_convert = GPLANtoGeomeppy(self.case, self.inputs.geometry)
        self.case.idf.intersect_match()
        self.case.idf.set_default_constructions()
        
        
    def get_geometry(self):
        self.case.get_geometry()
        self.zones = self.case.geometry.zones

    def update_geometry_walls(self):
        for zone in self.case.geometry.zones.values():
            self.case.geometry.walls.update(zone.walls)


    # TODO: this should probably go elsewhere.. 
    def get_subsurface_constructions(self):
        self.door_const = self.case.idf.getobject("CONSTRUCTION", "Project Door")
        self.window_const = self.case.idf.getobject("CONSTRUCTION", "Project External Window")

    def add_doors(self):
        standard_door = SubsurfaceAttributes(SubsurfaceObjects.DOOR, 1, 2, self.door_const) #type:ignore
        inputs = SubsurfaceInputs(self.zones, self.inputs.door_pairs, self.case.idf, standard_door)
        self.ss = SubsurfaceCreator(inputs)
        self.ss.create_all_ssurface()

    def add_windows(self):
        standard_window = SubsurfaceAttributes(SubsurfaceObjects.WINDOW, 0.5, 0.5, self.window_const) #type:ignore
        inputs = SubsurfaceInputs(self.zones, self.inputs.window_pairs, self.case.idf, standard_window)
        self.ss = SubsurfaceCreator(inputs)
        self.ss.create_all_ssurface()

    

    def update_geometry_subsurfaces(self):
        subsurfaces  = []
        for zone in self.case.geometry.zones.values():
            subsurfaces.extend(zone.get_subsurfaces())
        for subsurface in subsurfaces:
            self.case.geometry.subsurfaces.update({subsurface.bunch_name: subsurface})


    def add_airflownetwork(self):
        self.afn = AirflowNetwork(self.case)


    def add_output_variables(self):
        self.out_reqs = OutputRequests(self.case)
        for var in self.inputs.output_variables:
            self.out_reqs.add_output_variable(name=var.value)
        
        default_site_vars = [OV.site_db_temp, OV.site_diffuse_solar_rad, OV.site_direct_solar_rad,]
        all_vars = self.inputs.output_variables + default_site_vars
            
        self.eligible_vars = Munch()
        for var in all_vars:
            self.eligible_vars.update({var.name: var})
    

        self.out_reqs.request_sql()

    def make_base_plot(self):
        self.base_plot = Base2DPlot(self.case.geometry)
        self.base_plot.run()
     

    def prepare_plotter(self):
        sql_input = SQLInputs(self.inputs.case_name, self.case.geometry, self.inputs.output_variables)
        plotter_input = PlotterInputs(self.base_plot)

        try:
            self.plt = Plotter(plotter_input, sql_input)
        except AssertionError:
            print("No SQL file for this case")

        # TODO => handle no sql file exception (havent run the case yet.. )
        # TODO make sure sql file and idf match up somehow.. 
  

    def show_eligible_outputs(self):
        pprint({k:v.value for k,v in self.eligible_vars.items()})

    def show_base_plot(self):
        self.base_plot.fig.show()






