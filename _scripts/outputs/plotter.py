# from outputs.sql import SQLReader
from outputs.line_plots import LinePlot
from outputs.surface_2d import Surface2DPlot
from outputs.input_classes import LinePlotInputs, PlotTypes, PlotterInputs, Surface2DPlotInputs, SQLInputs
from outputs.sql import SQLReader
from datetime import time


class Plotter(SQLReader):
    def __init__(self, inputs: PlotterInputs, sql_inputs: SQLInputs) -> None:
        super().__init__(sql_inputs)
        self.pinputs = inputs

    """
    TO RUN:
    self.get_collection_for_variable(ez.eligible_vars...)
    (maybe) self.show_analysis_periods()
    self.set_analysis_period(1)
    self.create_plot(plot_type)

    self ~ ez.plt
    """


    def create_plot(self, plot_type=PlotTypes.LINE, time:time=time(0,0)):
        self.prepare_for_plot()

        if plot_type == PlotTypes.LINE:
            self.line_plot_obj = LinePlot(
                LinePlotInputs(self.filtered_collection, self.geom_type)
            )
            self.line_plot_obj.create_plot()
            self.line_plot_obj.fig.show()

        elif plot_type == PlotTypes.SURFACE_2D:
            self.surface_2d_plot_obj = Surface2DPlot(Surface2DPlotInputs(
                self.filtered_collection,
                self.inputs.geometry,
                time,
                self.pinputs.base2D
            ))
            self.surface_2d_plot_obj.create_figure()
            self.surface_2d_plot_obj.fig.show()
        
        else: 
            raise Exception("Invalid plot type needs to be part of PlotTypes")
