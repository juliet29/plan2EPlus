# from outputs.sql import SQLReader
from outputs.line_plots import LinePlot
from outputs.surface_2d import Surface2DPlot
from outputs.input_classes import (
    LinePlotInputs,
    PlotTypes,
    PlotterInputs,
    Surface2DPlotInputs,
    SQLInputs,
)
from outputs.sql import SQLReader
from datetime import time


class Plotter(SQLReader):
    """
    TO RUN:
    self.get_collection_for_variable(ez.eligible_vars...)
    (maybe) self.show_analysis_periods()
    (maybe) self.set_analysis_period(1)
    self.create_plot(plot_type)

    self ~ ez.plt
    """

    def __init__(self, inputs: PlotterInputs, sql_inputs: SQLInputs) -> None:
        super().__init__(sql_inputs)
        self.pinputs = inputs

    def create_plot(
        self, plot_type=PlotTypes.LINE, time: time = time(0, 0), SHOW_FIG=True
    ):
        self.filter_collections()

        if plot_type == PlotTypes.LINE:
            self.get_collection_geometry_type(self.filtered_collection[0])
            self.line_plot_obj = LinePlot(
                LinePlotInputs(self.filtered_collection, self.geom_type)
            )
            self.handle_plotting(self.line_plot_obj, SHOW_FIG)

        elif plot_type == PlotTypes.SURFACE_2D:
            self.surface_2d_plot_obj = Surface2DPlot(
                Surface2DPlotInputs(
                    self.filtered_collection,
                    self.inputs.geometry,
                    time,
                    self.pinputs.base2D,
                )
            )
            self.handle_plotting(self.surface_2d_plot_obj, SHOW_FIG)

        else:
            raise Exception("Invalid plot type needs to be part of PlotTypes")

        return self.fig

    def handle_plotting(self, obj, SHOW_FIG):
        obj.create_plot()
        if SHOW_FIG:
            obj.fig.show()
        self.fig = obj.fig
