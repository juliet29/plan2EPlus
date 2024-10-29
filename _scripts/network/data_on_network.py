from pathlib import Path
from geomeppy import IDF
import polars as pl
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import Colormap, LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.axes import Axes
from itertools import accumulate

from helpers.ep_geom_helpers import get_zone_domains
from helpers.geometry_interfaces import Domain
from network.network import create_base_graph, create_multi_graph
from setup.data_wrangle import create_dataframe_for_all_cases, get_plot_labels, join_any_data
from setup.interfaces import CaseData


# def normalize_to_target(arr:pl.Series, t_min=0, t_max=1):
#     # log scale might be better..
#     r_min, r_max = arr.min(), arr.max()
#     normalize = lambda x: (x - r_min) / (r_max - r_min) # type: ignore
#     scale = lambda x: (normalize(x) * (t_max - t_min)) + t_min
#     return [scale(i) for i in arr]


def is_medians_df(medians: pl.DataFrame):
    assert medians.schema == pl.Schema(
        [("space_names", pl.String), ("values", pl.Float64), ("values_0", pl.Float64)]
    )


def get_domains_lim(zone_domains: list[Domain]):
    PAD = 1.4 * 1.1
    min_x = min([i.width.min for i in zone_domains]) - PAD
    max_x = max([i.width.max for i in zone_domains]) + PAD
    min_y = min([i.height.min for i in zone_domains]) - PAD
    max_y = max([i.height.max for i in zone_domains]) + PAD
    return (min_x, max_x), (min_y, max_y)


def get_matching_edge(G: nx.DiGraph, subsurface_name: str):
    for e in G.edges:
        if G.edges[e].get("subsurfaces").upper() == subsurface_name:
            return e
    raise Exception(f"No match for {subsurface_name} in {G.edges}")

def get_min_max_values(medians: pl.DataFrame):
    is_medians_df(medians)
    numeric_values = medians.select(pl.selectors.numeric())
    min_val = numeric_values.min_horizontal().min()
    max_val = numeric_values.max_horizontal().max()

    return min_val, max_val


def get_medians_data(case_data: list[CaseData], curr_case: CaseData, qois: list[str]):
    df = create_dataframe_for_all_cases(case_data, qois[0])
    df1 = join_any_data(df, case_data, qois[1])
    df_case = df1.filter(pl.col("case_names") == curr_case.case_name)
    return df_case.group_by(pl.col("space_names")).agg(
        pl.col(["values", "values_0"]).median()
    )



def init_multigraph(idf: IDF, path_to_input: Path):
    G, pos = create_base_graph(idf, path_to_input)
    Gm = create_multi_graph(G)
    return Gm, pos


def plot_zone_domains(idf: IDF):
    zone_domains = get_zone_domains(idf)
    xlim, ylim = get_domains_lim(zone_domains)
    fig, ax = plt.subplots()

    for d in zone_domains:
        ax.add_artist(d.get_mpl_patch())

    ax.set(xlim=xlim, ylim=ylim)

    return fig, ax


def plot_nodes(Gm: nx.MultiDiGraph, pos, ax: Axes):
    _ = nx.draw_networkx_nodes(Gm, pos, ax=ax)
    p = nx.draw_networkx_labels(Gm, pos, ax=ax, font_size=8)
    return ax


def plot_edges(Gm: nx.MultiDiGraph, pos, ax: Axes, medians: pl.DataFrame, cmap: Colormap):
    is_medians_df(medians)
    forward_edges = [get_matching_edge(Gm, s) for s in medians["space_names"]]
    
    rev_edges = [(e[1], e[0], e[2]) for e in forward_edges]

    min_val, max_val = get_min_max_values(medians)
    connectionstyle = [f"arc3,rad={r}" for r in [0.05] * 2]

    def plot_one_direction_edges(edges, values, ix):
        
        _ = nx.draw_networkx_edges(
            Gm,
            pos,
            edgelist=edges,
            edge_color=values,
            edge_cmap=cmap,
            edge_vmin=min_val, # type: ignore
            edge_vmax=max_val, # type: ignore
            connectionstyle=connectionstyle[ix],
            width=2,
            ax=ax,
        )
    plot_one_direction_edges(forward_edges, medians["values"], 0)
    plot_one_direction_edges(rev_edges, medians["values_0"], 1)

    return ax


def set_axis_ticks(ax: Axes):
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_major_locator(ticker.AutoLocator())

    return ax

def create_data_on_network_fig(case_data:list[CaseData], curr_case: CaseData, qois: list[str]):
    medians = get_medians_data(case_data, curr_case, qois)
    Gm, pos = init_multigraph(curr_case.idf, curr_case.path_to_input)

    min_val, max_val = get_min_max_values(medians)
    cmap = plt.get_cmap("Blues")

    fig, ax = plot_zone_domains(curr_case.idf)
    ax = plot_nodes(Gm, pos, ax)
    ax = plot_edges(Gm, pos, ax, medians, cmap)
    ax = set_axis_ticks(ax)

    case_info, qoi_info = get_plot_labels(curr_case, qois[0])
    norm = Normalize(vmin=min_val, vmax=max_val) # type: ignore
    fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=qoi_info)
    fig.suptitle(case_info)

    return fig




    


# G, pos = create_base_graph(idf, path_to_input)
# G_afn = create_afn_graph(idf, G)
# f = draw_afn_over_init(G, G_afn, pos)


# medians = df.group_by(pl.col("space_names")).agg(pl.col("values").median())
# filtered_medians = medians.filter(pl.col("values") > 0)
# filtered_medians

# values = normalize_to_target(filtered_medians["values"], t_min=1, t_max=4)
# edges = [get_matching_edge(G, s) for s in filtered_medians["space_names"]]

# f = draw_afn_over_init(G, G_afn, pos)
# patches = nx.draw_networkx_edges(G, pos, edges, values)
# f.suptitle(curr_qoi)


# connectionstyle = [f"arc3,rad={r}" for r in accumulate([0.15] * 2)]
# nx.draw_networkx_nodes(Gm, pos)
# p = nx.draw_networkx_labels(Gm, pos)
# p = nx.draw_networkx_edges(Gm, pos, connectionstyle=connectionstyle)
