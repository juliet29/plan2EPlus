from pathlib import Path
from geomeppy import IDF
import polars as pl
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import Colormap, Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from matplotlib.axes import Axes

from helpers.ep_geom_helpers import get_zone_domains
from helpers.geometry_interfaces import Domain
from network.network import create_base_graph, create_multi_graph
from setup.data_wrangle import create_dataframe_for_all_cases, get_plot_labels, join_any_data, join_site_data
from setup.interfaces import CaseData

DEG_SPLIT = 180

# def is_medians_df(medians: pl.DataFrame):
#     assert medians.schema == pl.Schema(
#         [("space_names", pl.String), ("values", pl.Float64), ("values_0", pl.Float64)])


def get_domains_lim(zone_domains: list[Domain]):
    PAD = 1.4 * 1.1
    min_x = min([i.width.min for i in zone_domains]) - PAD
    max_x = max([i.width.max for i in zone_domains]) + PAD
    min_y = min([i.height.min for i in zone_domains]) - PAD
    max_y = max([i.height.max for i in zone_domains]) + PAD
    return (min_x, max_x), (min_y, max_y)


def get_matching_edge(G: nx.MultiDiGraph, subsurface_name: str, value:float):
    consider_reverse = True if value >= 0 else False
    print(value, consider_reverse)
    for e in G.edges:
        if consider_reverse:
            if G.edges[e].get("reverse"):
                if G.edges[e].get("subsurfaces").upper() == subsurface_name:
                    return e
        else:
            if G.edges[e].get("subsurfaces").upper() == subsurface_name:
                    return e

    raise Exception(f"No match for {subsurface_name} in {G.edges}")

def get_min_max_values(medians: pl.DataFrame):
    # is_medians_df(medians)
    numeric_values = medians.select(pl.selectors.numeric())
    min_val = numeric_values.min_horizontal().min()
    max_val = numeric_values.max_horizontal().max()

    return min_val, max_val


def get_medians_data(case_data: list[CaseData], curr_case: CaseData, qois: list[str], low_wind_dir=True):
    qoi3 = "Site Wind Direction"
    df = create_dataframe_for_all_cases(case_data, qois[0])
    df1 = join_any_data(df, case_data, qois[1])
    df2 = join_site_data(curr_case, qoi3, df1, 1 )
    df3 = df2.with_columns(linkage=pl.col("values") - pl.col("values_0"))
    df_case = df3.filter(pl.col("case_names") == curr_case.case_name)

    df_north_east = df_case.filter(pl.col("values_1").is_between(0,15)  )
    df_north_west = df_case.filter(pl.col("values_1").is_between(345, 360))

    # medians = df_case.group_by(pl.col("space_names")).agg(
    #         pl.col(["values", "values_0", "linkage"]).median()
    #     )


    # return medians

    df_wind = df_north_east if low_wind_dir else df_north_west


    df_case = df_wind.filter(pl.col("case_names") == curr_case.case_name)
    return df_case.group_by(pl.col("space_names")).agg(
        pl.col(["values", "values_0", "linkage"]).median()
    )



def init_multigraph(idf: IDF, path_to_input: Path):
    G, pos = create_base_graph(idf, path_to_input)
    Gm = create_multi_graph(G)
    return Gm, pos


def plot_zone_domains(idf: IDF, ax: Axes):
    zone_domains = get_zone_domains(idf)
    xlim, ylim = get_domains_lim(zone_domains)
    # fig, ax = plt.subplots()

    for d in zone_domains:
        ax.add_artist(d.get_mpl_patch())

    ax.set(xlim=xlim, ylim=ylim)

    return ax


def plot_nodes(Gm: nx.MultiDiGraph, pos, ax: Axes):
    _ = nx.draw_networkx_nodes(Gm, pos, ax=ax)
    p = nx.draw_networkx_labels(Gm, pos, ax=ax, font_size=8)
    return ax


def plot_edges(Gm: nx.MultiDiGraph, pos, ax: Axes, medians: pl.DataFrame, cmap: Colormap):
    # is_medians_df(medians)
    match_edges = [get_matching_edge(Gm, s, v) for s, v in zip(medians["space_names"], medians["linkage"])]
    
    rev_edges = [(e[1], e[0], e[2]) for e in match_edges]

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
    plot_one_direction_edges(match_edges, medians["values"], 0)
    # plot_one_direction_edges(rev_edges, medians["values_0"], 1)

    return ax


def set_axis_ticks(ax: Axes):
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_major_locator(ticker.AutoLocator())

    return ax

# def create_data_on_network_fig(case_data:list[CaseData], curr_case: CaseData, qois: list[str], low_wind_dir=True):
#     medians = get_medians_data(case_data, curr_case, qois, low_wind_dir)
#     Gm, pos = init_multigraph(curr_case.idf, curr_case.path_to_input)

#     min_val, max_val = get_min_max_values(medians)
#     cmap = plt.get_cmap("Blues")
#     norm = Normalize(vmin=min_val, vmax=max_val) # type: ignore

#     fig, ax = plot_zone_domains(curr_case.idf)
#     ax = plot_nodes(Gm, pos, ax)
#     ax = plot_edges(Gm, pos, ax, medians, cmap)
#     ax = set_axis_ticks(ax)

#     case_info, qoi_info = get_plot_labels(curr_case, qois[0])
#     fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=qoi_info)
#     fig.suptitle(f"{case_info}: < 100º? {low_wind_dir}")

#     return fig

def true_min_max(min_max_pairs: list[tuple[float, float]]):
    min_val = min([m[0] for m in min_max_pairs])
    max_val = max([m[1] for m in min_max_pairs])
    return min_val, max_val


def create_data_on_network_fig_facet_winddir(case_data:list[CaseData], curr_case: CaseData, qois: list[str]):
    Gm, pos = init_multigraph(curr_case.idf, curr_case.path_to_input)

    low_wind_dir_vals = [True, False]
    medians = [get_medians_data(case_data, curr_case, qois, i) for i in low_wind_dir_vals]
    min_max_pairs = [get_min_max_values(i) for i in medians]
    min_val, max_val = true_min_max(min_max_pairs) # type: ignore


    colors = ["#9ee6f7", "#001f26"]
    cmap = LinearSegmentedColormap.from_list("customBlues", colors)
    # cmap = plt.get_cmap("Blues").resampled(20)
    norm = Normalize(vmin=min_val, vmax=max_val) # type: ignore

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    for ax, median, windir in zip(axes, medians, low_wind_dir_vals): # type: ignore
        ax = plot_zone_domains(curr_case.idf, ax)
        ax = plot_nodes(Gm, pos, ax)
        ax = plot_edges(Gm, pos, ax, median, cmap)
        ax = set_axis_ticks(ax)
        drn = "NORTH_EAST" if windir else "NORTH_WEST"
        ax.set_title(f" {drn}")


    case_info, qoi_info = get_plot_labels(curr_case, qois[0])
    fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=qoi_info)
    fig.suptitle(f"{case_info}")

    return fig

