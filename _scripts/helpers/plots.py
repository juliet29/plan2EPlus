import shapely as sp
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def get_plottable_coords(coords: sp.coords.CoordinateSequence):
    x = [c[0] for c in coords]
    y = [c[1] for c in coords]
    return x, y

class RectFromCoords:
    # ref: https://plotly.com/python/reference/layout/shapes/#layout-shapes-items-shape-x0
    def __init__(self, coords: sp.coords.CoordinateSequence) -> None:
        xs = [i[0]for i in coords]
        ys = [i[1]for i in coords]
        # self.x0 = min(xs)
        # self.x1 = max(xs)
        # self.y0 = min(ys)
        # self.y1 = max(ys)
        self.x0 = coords[0][0]
        self.x1 = coords[2][0]
        self.y0 = coords[0][1]
        self.y1 = coords[1][1]

    def __repr__(self):
        return f"Rect(({self.x0}, {self.y0}), ({self.x1}, {self.y1}))"

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

def get_norm_plotly_colors(sample_pts, min, max, color_scheme="turbo"):
    return px.colors.sample_colorscale(colorscale=color_scheme, samplepoints=sample_pts, low=min, high=max)



def plot_line_string(line: sp.LineString, color="yellow", label=None, width=3):
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


def plot_rectangle_shape(polygon: sp.Polygon, color="blue", label=None):
    r = RectFromCoords(polygon.exterior.coords)
    d = dict(type="rect",
    xref="x", yref="y",
    fillcolor=color,
    x0=r.x0,
    y0=r.y0,
    x1=r.x1,
    y1=r.y1,
    label=dict(text=label))

    return d 

def create_colorbar(min, max, color_scheme="turbo", ):
    # TODO make ticks dynamic.. 
    trace = go.Scatter(
        # hoverinfo='none'
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(
            colorscale=color_scheme, 
            showscale=True,
            cmin=min,
            cmax=max,
            colorbar=dict(thickness=5, tickvals=np.linspace(min, max, 5), ticktext=[round(min, 3), round(max,3)], outlinewidth=0)
        ))
    return trace