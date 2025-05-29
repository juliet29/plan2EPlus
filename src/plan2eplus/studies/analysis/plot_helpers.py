from typing import Iterable
import random
import matplotlib.ticker as ticker
from matplotlib.colors import Colormap, Normalize
from matplotlib.cm import ScalarMappable
import networkx as nx

from plan2eplus.helpers.geometry_interfaces import Domain
from ...helpers.ep_geom_helpers import get_zone_domains

import polars as pl

from geomeppy import IDF
from matplotlib.axes import Axes


def get_domains_lim(zone_domains: list[Domain], PAD_BASE=1.4):
    PAD = PAD_BASE * 1.1
    min_x = min([i.horz_range.min for i in zone_domains]) - PAD
    max_x = max([i.horz_range.max for i in zone_domains]) + PAD
    min_y = min([i.vert_range.min for i in zone_domains]) - PAD
    max_y = max([i.vert_range.max for i in zone_domains]) + PAD
    return (min_x, max_x), (min_y, max_y)


def plot_zone_domains(idf: IDF, ax: Axes):
    zone_domains = get_zone_domains(idf)
    xlim, ylim = get_domains_lim(zone_domains)
    for d in zone_domains:
        ax.add_artist(d.get_mpl_patch())

    ax.set(xlim=xlim, ylim=ylim)

    return ax


def plot_nodes_simple(Gm: nx.MultiDiGraph, pos, ax: Axes):
    _ = nx.draw_networkx_nodes(Gm, pos, ax=ax)
    _ = nx.draw_networkx_labels(Gm, pos, ax=ax, font_size=8)
    return ax


def plot_nodes(
    Gm: nx.MultiDiGraph,
    pos,
    ax: Axes,
    nodes: Iterable[str],
    values: Iterable[float],
    cmap: Colormap,
    min_max: tuple,
):
    vmin, vmax = min_max
    _ = nx.draw_networkx_nodes(
        Gm,
        pos,
        ax=ax,
        nodelist=nodes,
        node_color=values,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        node_size=400,
    )  # type: ignore
    _ = nx.draw_networkx_labels(
        Gm,
        pos,
        ax=ax,
        font_size=8,
        font_weight="bold",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
    )
    return ax


def plot_edges_widths(
    Gm: nx.MultiDiGraph, pos, ax: Axes, edges: Iterable[str], values: Iterable[float]
):
    _ = nx.draw_networkx_edges(
        Gm,
        pos,
        edgelist=edges,
        width=values,  # type: ignore
        # edge_color=values,
        ax=ax,
        alpha=1,
        arrowsize=30,
        # min_target_margin=15
    )
    return ax


def plot_edge_labels(
    Gm: nx.MultiDiGraph, pos, ax: Axes, edges: pl.Series, values: pl.Series
):
    edges_map = {
        tuple(k): round(v, 2) for k, v in zip(edges.to_list(), values.to_list())
    }
    _ = nx.draw_networkx_edge_labels(
        Gm, pos, edge_labels=edges_map, ax=ax, font_size=7, rotate=False
    )
    return ax


def set_axis_ticks(ax: Axes):
    ax.xaxis.set_ticks_position("bottom")
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_ticks_position("left")
    ax.yaxis.set_major_locator(ticker.AutoLocator())

    return ax


def create_colorbar(fig, ax, cmap, min_max: tuple, qoi_info: str):
    norm = Normalize(*min_max)  # type: ignore
    fig.colorbar(
        ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=qoi_info, location="bottom"
    )
    return fig
