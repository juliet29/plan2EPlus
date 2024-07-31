from dataclasses import dataclass
from geometry.geometry_parser import GeometryParser
from outputs.variables import OutputVars
from typing import List
from outputs.base_2d import Base2DPlot
from datetime import time
from enum import Enum




@dataclass
class LinePlotInputs:
    collection_by_ap: List  # only one analysis period
    geom_type: str


@dataclass
class Surface2DPlotInputs:
    collection_by_ap: List 
    geometry: GeometryParser
    plot_time: time
    base2D: Base2DPlot 


class PlotTypes(Enum):
    LINE = 0
    SURFACE_2D = 1


@dataclass
class SQLInputs:
    case_name: str
    path: str
    geometry: GeometryParser
    output_variables: List[OutputVars]
    project_name:str = ""
    


@dataclass
class PlotterInputs:
    base2D: Base2DPlot 
