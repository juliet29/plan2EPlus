import os
from dataclasses import dataclass
from munch import Munch
from datetime import time
from jinja2 import Template

from outputs.plotter import Plotter
from outputs.base_2d import Base2DPlot
from outputs.input_classes import PlotTypes


INPUT_TEMPLATE_PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/geomeppy/_scripts/workflow/auto_analysis.html.j2"


@dataclass
class AutoAnalysisInputs:
    variable_names: Munch  # only one analysis period
    plotter: Plotter
    base_plot: Base2DPlot
    case_name: str
    path: str


class AutoAnalysis:
    def __init__(self, inputs: AutoAnalysisInputs) -> None:
        self.inputs = inputs
        self.vars = inputs.variable_names
        self.plt = inputs.plotter
        self.run()
        

    def run(self):
        self.initialize_plotter()
        self.create_variable_groups()
        self.create_jinja_data()
        self.create_html_file()


    def create_variable_groups(self):
        v = self.vars

        self.site_data_vars = [v.site_db_temp, v.site_wind_direction, v.site_wind_speed]

        self.afn_data_vars = [v.zone_ach,v.zone_vent_heat_gain, v.zone_vent_heat_loss, v.linkage_flow12, v.linkage_flow21]

        self.surface_data_vars = [v.surf_inside_temp, v.surf_outside_temp, v.surf_incident_solar_rad]

        self.groups = [self.site_data_vars, self.afn_data_vars, self.surface_data_vars]
        self.group_names = ["site_data_vars", "afn_data_vars", "surface_data_vars"]


    def create_jinja_data(self):
        self.plotly_jinja_data = {name:self.make_fig_list(group) for name, group in zip(self.group_names, self.groups)}

        self.plotly_jinja_data["surface_data_2D_vars"] = self.make_fig_list(self.surface_data_vars, _2D=True)

        self.plotly_jinja_data["base_plot"] = self.inputs.base_plot.fig.to_html(full_html=False)

        self.plotly_jinja_data["case_name"] = self.inputs.case_name # type: ignore


    def initialize_plotter(self):
        self.plt.get_collection_for_variable(self.vars.zone_mean_air_temp)
        self.plt.set_analysis_period(0)


    def create_html_file(self):
        output_html_path = os.path.join(self.inputs.path, "analysis.html")
        with open(output_html_path, "w+", encoding="utf-8") as output_file:
            with open(INPUT_TEMPLATE_PATH ) as template_file:
                j2_template = Template(template_file.read())
                output_file.write(j2_template.render(self.plotly_jinja_data))



    def make_fig(self, var):
        self.plt.get_collection_for_variable(var)
        return self.plt.create_plot(SHOW_FIG=False).to_html(full_html=False)


    def make_2D_fig(self, var):
        self.plt.get_collection_for_variable(var)
        return self.plt.create_plot(PlotTypes.SURFACE_2D, time(12,0), SHOW_FIG=False).to_html(full_html=False)


    def make_fig_list(self, group, _2D=False):
        if _2D:
            return [self.make_2D_fig(var) for  var in group]
        else:
            return [self.make_fig(var) for  var in group]