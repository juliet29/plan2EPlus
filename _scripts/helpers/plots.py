from typing import TypedDict
import plotly.graph_objects as go
import numpy as np

class ShapeDict(TypedDict):
    type: str
    xref: str
    yref: str
    fillcolor: str
    x0: float
    y0: float
    x1: float
    y1: float
    label: dict[str, str]


def plot_one_shape(trace_dict: ShapeDict, fig=None):
    if not fig:
        fig = go.Figure()
    fig.add_shape(**trace_dict)
    return fig


def plot_many_shapes(
    dict_of_trace_dict: dict[str, ShapeDict],
    x_range: list | None = None,
    y_range: list | None = None,
    fig_width: float = 0,  # 400..
    fig_height: float = 0,
    padding: int = 50,
    fig=None,
    title=None,
):
    if not fig:
        fig = go.Figure()
    for trace_dict in dict_of_trace_dict.values():
        fig.add_shape(**trace_dict)

    if x_range and y_range:
        fig.update_xaxes(range=x_range)
        fig.update_yaxes(range=y_range)

    if fig_height and fig_width:
        fig.update_layout(
            autosize=False,
            width=fig_width,
            height=fig_height,
            margin=dict(l=padding, r=padding, b=padding, t=padding, pad=4), # TODO what is pad?
        )

    if title:
        fig.update_layout(title=title)

    return fig


def create_colorbar(
    min,
    max,
    color_scheme="turbo",
):
    # TODO make ticks dynamic..
    trace = go.Scatter(
        # hoverinfo='none'
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(
            colorscale=color_scheme,
        showscale=True,
            cmin=min,
            cmax=max,
            colorbar=dict(
                thickness=5,
                tickvals=[round(i, 2) for i in np.linspace(min, max, 5)],
                ticktext=[round(min, 2), round(max, 2)],
                outlinewidth=0,
            ),
        ),
    )
    return trace


def create_range_limits(trace_dict: dict, buffer=10):
    xrange = [trace_dict["x0"] - buffer, trace_dict["x1"] + buffer]
    yrange = [trace_dict["y0"] - buffer, trace_dict["y1"] + buffer]

    return xrange, yrange




