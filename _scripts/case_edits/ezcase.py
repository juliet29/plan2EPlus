from dataclasses import dataclass
import os
import dataclasses
from operator import attrgetter
from typing import List, Tuple, Union, Sequence
from munch import Munch

from new_subsurfaces.interfaces import SubsurfaceAttributes, SubsurfaceType
from plan.convert import PlantoGeomeppy

from case_edits.epcase import EneryPlusCaseEditor
from helpers.special_types import GeometryType

from methods.subsurfaces.inputs import SubsurfaceCreatorInputs
from new_subsurfaces.interfaces import SubsurfacePair
from methods.subsurfaces.creator import SubsurfaceCreator

from methods.airflownetwork import AirflowNetwork
from methods.outputs import OutputRequests

from outputs.variables import OutputVars as OV
from outputs.input_classes import SQLInputs, PlotterInputs
from outputs.plotter import Plotter
from outputs.sql import SQLReader
from outputs.base_2d import Base2DPlot

from workflow.auto_analysis import AutoAnalysis, AutoAnalysisInputs
from analysis.post_process import PostProcesser

from pprint import pprint, pformat


class EzCase:
    def __init__(self, input: EzCaseInput, RUN_CASE=False) -> None:
        self.inputs = input
        self.RUN_CASE = RUN_CASE
        self.format_inputs()
        # self.run()

    def __repr__(self):
        return self.sinput_vals

    def run(self):
        self.create_case()
        self.add_rooms()
        self.add_subsurfaces()
        self.add_airflownetwork()
        self.add_output_variables()
        self.case.compare_and_save()
        if self.RUN_CASE:
            self.case.run_idf()
        self.make_base_plot()
        self.prepare_plotter()
        if self.RUN_CASE:
            # self.run_analysis()
            self.post_process_variables()

    def create_case(self):
        self.case = EneryPlusCaseEditor(
            self.inputs.case_name,
            self.inputs.starting_case,
            project_name=self.inputs.project_name,
        )
        print(self.inputs.case_name)

    def add_rooms(self):
        self.gplan_convert = PlantoGeomeppy(self.case, self.inputs.geometry)
        self.case.idf.intersect_match()
        self.case.idf.set_default_constructions()
        self.get_geometry()

    def get_geometry(self):
        self.case.get_geometry()
        self.zones = self.case.geometry.zones
        self.case.geometry.update_geometry_walls()

    def add_subsurfaces(self):
        if self.inputs.subsurface_pairs:
            self.get_subsurface_constructions()
            inputs = SubsurfaceCreatorInputs(
                self.zones, self.inputs.subsurface_pairs, self.case.idf
            )
            self.ss = SubsurfaceCreator(inputs)
            self.ss.run()
            self.case.geometry.update_geometry_subsurfaces()

    def add_airflownetwork(self):
        if self.inputs.subsurface_pairs:
            self.afn = AirflowNetwork(self.case)

    def add_output_variables(self):
        self.out_reqs = OutputRequests(self.case)
        self.out_reqs.request_advanced_variables()
        self.out_reqs.request_sql()

        for var in self.inputs.output_variables:
            self.out_reqs.add_output_variable(name=var.value)

        default_site_vars = [
            OV.site_db_temp,
            OV.site_diffuse_solar_rad,
            OV.site_direct_solar_rad,
        ]
        all_vars = self.inputs.output_variables + default_site_vars
        self.eligible_vars = Munch()
        for var in all_vars:
            self.eligible_vars.update({var.name: var})

    def make_base_plot(self):
        self.base_plot = Base2DPlot(self.case.geometry, self.case.case_name)
        self.base_plot.run()

    def prepare_plotter(self):
        sql_input = SQLInputs(
            self.inputs.case_name,
            self.case.path,
            self.case.geometry,
            self.inputs.output_variables,
            self.inputs.project_name,
        )
        plotter_input = PlotterInputs(self.base_plot)

        if "results" in next(os.walk(self.case.path))[1]:
            results_path = os.path.join(self.case.path, "results")
            if "eplusout.sql" in next(os.walk(results_path))[2]:
                print("looking for sql")
                self.sql = SQLReader(sql_input)
                self.plt = Plotter(plotter_input, sql_input)
                assert self.plt is not None
            else:
                print("No SQL file")
                # self.plt = None
        else:
            print("No results")
            # self.plt = None

    def post_process_variables(self):
        if self.sql:
            self.post_processer = PostProcesser(self.sql, self.case.path)
            self.post_processer.calc_defaults()
        else:
            print("not post processing")

    def run_analysis(self):
        if self.plt:
            print("running analysis")
            inputs = AutoAnalysisInputs(
                self.eligible_vars,
                self.plt,
                self.base_plot,
                self.inputs.case_name,
                self.case.path,
            )
            self.analysis = AutoAnalysis(inputs)
        else:
            print("Plotter object was not created, so no analysis performed")

    def show_eligible_outputs(self):
        pprint({k: v.value for k, v in self.eligible_vars.items()})

    def show_base_plot(self):
        self.base_plot.fig.show()

    ## helpers
    def format_inputs(self):
        self.input_vals = {
            field.name: attrgetter(field.name)(self.inputs)
            for field in dataclasses.fields(self.inputs)
            if field.name != "output_variables"
        }
        self.sinput_vals = pformat(self.input_vals, sort_dicts=False)

    def get_subsurface_constructions(self):
        self.door_const = self.case.idf.getobject("CONSTRUCTION", "Project Door")
        self.window_const = self.case.idf.getobject(
            "CONSTRUCTION", "Project External Window"
        )
        # TODO temp - fix when do materials better.. ie make them importable from a default..
        for p in self.inputs.subsurface_pairs:
            assert type(p.attrs) == SubsurfaceAttributes
            if p.attrs.object_type == SubsurfaceType.DOOR:
                p.attrs.construction = self.door_const
            else:
                p.attrs.construction = self.window_const
