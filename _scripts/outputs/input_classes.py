from dataclasses import dataclass
from geometry.geometry_parser import GeometryParser
from outputs.variables import OutputVars 
from typing import List


@dataclass
class SQLInputs:
    case_name: str
    geometry: GeometryParser
    output_variables:List[OutputVars]

@dataclass
class PlotInputs:
    collection_by_ap: List
    geom_type: str

# @dataclass
# class Base2DPlotInputs:
#     zones: 