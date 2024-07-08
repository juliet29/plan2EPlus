from shapely import LineString, Polygon
from shapely.coords import CoordinateSequence
import plotly.graph_objects as go


class PlotCoords:
    # ref: https://plotly.com/python/reference/layout/shapes/#layout-shapes-items-shape-x0
    def __init__(self, coords: CoordinateSequence) -> None:
        x, y = get_plottable_coords(coords)
        self.x0 = min(x)
        self.x1 = max(x)
        self.y0 = min(y)
        self.y1 = max(y)

    def __repr__(self):
        return f"PlotCoords(({self.x0}, {self.y0}), ({self.x1}, {self.y1}))"


def get_plottable_coords(coords: CoordinateSequence):
    x = [c[0] for c in coords]
    y = [c[1] for c in coords]
    return x, y


def prepare_line_traces(line: LineString, color="yellow", label=None, width=3):
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


def prepare_polygon_trace(polygon: Polygon, color="blue", label=None):
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


def prepare_shape_dict(
    coords: CoordinateSequence,
    type="rect",
    color="blue",
    label="",
    width=3,
):
    r = PlotCoords(coords)
    d = dict(
        type=type,
        xref="x",
        yref="y",
        fillcolor=color,
        x0=r.x0,
        y0=r.y0,
        x1=r.x1,
        y1=r.y1,
        label=dict(text=label),
    )

    if type == "line":
        d["line"] = dict(color=color, width=width)  # type:ignore
        d["label_font_color"] = color
        d["label_font_size"] = 9  # type:ignore

    return d


def plot_shape(
    trace_dict: dict,
    x_range: list,
    y_range: list,
    fig_width: float=0,
    fig_height: float=0,
    padding: int = 50,
):
    fig = go.Figure()
    for trace in trace_dict.values():
        fig.add_shape(**trace)

    if x_range and y_range:
        fig.update_xaxes(range=x_range)
        fig.update_yaxes(range=y_range)

    if fig_height and fig_width:
        # TODO what is pad?
        fig.update_layout(
            autosize=False,
            width=fig_width,
            height=fig_height,
            margin=dict(l=padding, r=padding, b=padding, t=padding, pad=4),
        )
    return fig
