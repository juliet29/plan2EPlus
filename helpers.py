import sys
import os
import fnmatch
import re

from icecream import ic

from geomeppy import IDF
from geomeppy.patches import EpBunch


import shapely as sp
import plotly.graph_objects as go





#MARK: shapely helpers
def points_to_plot(coords):
    x = [c[0] for c in coords]
    y  = [c[1] for c in coords]
    return x, y


def plot_line_string(line:sp.LineString, color="yellow", label=None):
    x, y = points_to_plot(line.coords)
    trace = go.Scatter(x=x, y=y, mode='markers+lines', marker=dict(color=color),  line=dict(color=color), name=label)
    return trace




