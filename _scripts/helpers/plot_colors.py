import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def get_plotly_colors(n_colors=10, color_scheme="turbo"):
    colors = px.colors.sample_colorscale(
        color_scheme, [n / (n_colors - 1) for n in range(n_colors)]
    )
    return colors, iter(colors)


def get_norm_plotly_colors(sample_pts, min, max, color_scheme="turbo"):
    return px.colors.sample_colorscale(
        colorscale=color_scheme, samplepoints=sample_pts, low=min, high=max
    )



def study_colors(n=6, color_scheme="Agsunset"):
    colors, _ = get_plotly_colors(n_colors=n, color_scheme=color_scheme)
    ys = np.linspace(0, 100, n)

    fig = go.Figure()

    for y, c in zip(ys, colors):
        fig.add_trace(
            go.Scatter(
                y=[y],
                x=[y],
                mode="markers",
                marker=dict(
                    size=12,
                    color=c,  # set color equal to a variable
                ),
            )
        )

    return fig