from typing import Iterable
import matplotlib.ticker as ticker
from matplotlib.colors import Colormap, Normalize
from matplotlib.cm import ScalarMappable
import networkx as nx
from analysis.helpers import get_domains_lim
from helpers.ep_geom_helpers import get_zone_domains


from geomeppy import IDF
from matplotlib.axes import Axes


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

def plot_nodes(Gm: nx.MultiDiGraph, pos, ax: Axes, nodes: Iterable[str], values:Iterable[float], cmap: Colormap, min_max:tuple):
    vmin, vmax = min_max
    _ = nx.draw_networkx_nodes(Gm, pos, ax=ax, nodelist=nodes, node_color=values, cmap=cmap, vmin=vmin, vmax=vmax)  # type: ignore
    _ = nx.draw_networkx_labels(Gm, pos, ax=ax, font_size=8)
    return ax

def set_axis_ticks(ax: Axes):
    ax.xaxis.set_ticks_position("bottom")
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_ticks_position("left")
    ax.yaxis.set_major_locator(ticker.AutoLocator())

    return ax

def create_colorbar(fig, ax, cmap, min_max:tuple, qoi_info:str):
    norm = Normalize(*min_max)  # type: ignore
    fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=qoi_info)
    return fig



