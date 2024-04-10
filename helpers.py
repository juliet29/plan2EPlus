import sys
import os
import fnmatch
import re

from icecream import ic

from geomeppy import IDF
from geomeppy.patches import EpBunch


import shapely as sp
import plotly.graph_objects as go
import plotly.express as px


def get_plottable_coords(coords: sp.coords.CoordinateSequence):
    x = [c[0] for c in coords]
    y = [c[1] for c in coords]
    return x, y

def get_plotly_colors(n_colors=10, color_scheme="turbo"):
    """
    rainbow like: turbo, jet
    for-non rainbow, should change n_colors to match # of items!
    sequential: purp, mint, ...
    """
    colors = px.colors.sample_colorscale(
        color_scheme, [n / (n_colors - 1) for n in range(n_colors)]
    )

    return colors, iter(colors)


def plot_line_string(line: sp.LineString, color="yellow", label=None, width=5):
    x, y = get_plottable_coords(line.coords)
    trace = go.Scatter(
        x=x,
        y=y,
        mode="markers+lines",
        marker=dict(color=color),
        line=dict(color=color, width=width),
        name=label,
    )
    return trace

def plot_polygon(polygon: sp.Polygon, color="blue", label=None):
    x, y = get_plottable_coords(polygon.exterior.coords)
    trace = go.Scatter(
        x=x,
        y=y,
        fill="toself",
        marker=dict(color=color),
        fillcolor=color, 
        opacity=0.5,
        line_width=0,
        name=label,
        
    )
    return trace


##MARK: text editing 
def get_last_word(string):
  
    # split by space and converting 
    # string to list and
    lis = list(string.split(" "))
    
    # length of list
    length = len(lis)
    
    # returning last element in list
    return lis[length-1]


