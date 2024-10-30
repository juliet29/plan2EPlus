from pathlib import Path
from geomeppy import IDF
import polars as pl
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import Colormap, Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.axes import Axes

from helpers.ep_geom_helpers import get_zone_domains
from helpers.geometry_interfaces import Domain
from network.network import create_base_graph, create_multi_graph
from setup.data_wrangle import (
    create_dataframe_for_all_cases,
    get_plot_labels,
    join_any_data,
    join_site_data,
)
from setup.interfaces import CaseData
from setup.setup import retrieve_cases


def get_domains_lim(zone_domains: list[Domain]):
    PAD = 1.4 * 1.1
    min_x = min([i.width.min for i in zone_domains]) - PAD
    max_x = max([i.width.max for i in zone_domains]) + PAD
    min_y = min([i.height.min for i in zone_domains]) - PAD
    max_y = max([i.height.max for i in zone_domains]) + PAD
    return (min_x, max_x), (min_y, max_y)


def get_matching_edge(G: nx.MultiDiGraph, subsurface_name: str, value: float):
    consider_reverse = True if value < 0 else False

    for e in G.edges:
        if consider_reverse:
            if G.edges[e].get("reverse"):
                if G.edges[e].get("subsurfaces").upper() == subsurface_name:
                    return e
        else:
            if G.edges[e].get("subsurfaces").upper() == subsurface_name:
                if not G.edges[e].get("reverse"):
                    return e

    raise Exception(f"No match for {subsurface_name} in {G.edges}")


def get_min_max_values(medians: pl.DataFrame, col=None):
    # is_medians_df(medians)
    if not col:
        numeric_values = medians.select(pl.selectors.numeric())
        min_val = numeric_values.min_horizontal().min()
        max_val = numeric_values.max_horizontal().max()

    else:
        series = medians[col]
        return series.min(), series.max()

    return min_val, max_val


def get_medians_data(
    case_data: list[CaseData], curr_case: CaseData, qois: list[str], low_wind_dir=True
):
    qoi3 = "Site Wind Direction"
    df = create_dataframe_for_all_cases(case_data, qois[0])
    df1 = join_any_data(df, case_data, qois[1])
    df2 = join_site_data(curr_case, qoi3, df1, 1)
    df3 = df2.with_columns(linkage=pl.col("values") - pl.col("values_0"))
    df_case = df3.filter(pl.col("case_names") == curr_case.case_name)

    df_north_east = df_case.filter(pl.col("values_1").is_between(0, 15))
    df_north_west = df_case.filter(pl.col("values_1").is_between(345, 360))

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
    _ = nx.draw_networkx_labels(Gm, pos, ax=ax, font_size=8)
    return ax


def plot_edges(
    Gm: nx.MultiDiGraph,
    pos,
    ax: Axes,
    medians: pl.DataFrame,
    cmap: Colormap,
    color_lims: tuple,
):
    match_edges = [
        get_matching_edge(Gm, s, v)
        for s, v in zip(medians["space_names"], medians["linkage"])
    ]
    min_val, max_val = color_lims

    connectionstyle = f"arc3,rad={0.05}"

    def plot_one_direction_edges(edges, values):
        _ = nx.draw_networkx_edges(
            Gm,
            pos,
            edgelist=edges,
            edge_color=values,
            edge_cmap=cmap,
            edge_vmin=min_val,  # type: ignore
            edge_vmax=max_val,  # type: ignore
            connectionstyle=connectionstyle,
            width=2,
            ax=ax,
        )

    plot_one_direction_edges(match_edges, medians["linkage"])

    return ax


def set_axis_ticks(ax: Axes):
    ax.xaxis.set_ticks_position("bottom")
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_ticks_position("left")
    ax.yaxis.set_major_locator(ticker.AutoLocator())

    return ax


def true_min_max(min_max_pairs: list[tuple[float, float]]):
    min_val = min([m[0] for m in min_max_pairs])
    max_val = max([m[1] for m in min_max_pairs])
    return min_val, max_val


def create_data_on_network_fig_facet_winddir(
    case_data: list[CaseData], curr_case: CaseData, qois: list[str]
):
    Gm, pos = init_multigraph(curr_case.idf, curr_case.path_to_input)

    low_wind_dir_vals = [True, False]
    medians = [
        get_medians_data(case_data, curr_case, qois, i) for i in low_wind_dir_vals
    ]
    min_max_pairs = [get_min_max_values(i, "linkage") for i in medians]
    min_val, max_val = true_min_max(min_max_pairs)  # type: ignore

    # colors = ["#9ee6f7", "#001f26"]
    # cmap = LinearSegmentedColormap.from_list("customBlues", colors)
    cmap = plt.get_cmap("coolwarm")  # .resampled(20)
    norm = Normalize(vmin=min_val, vmax=max_val)  # type: ignore

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    for ax, median, windir in zip(axes, medians, low_wind_dir_vals):  # type: ignore
        ax = plot_zone_domains(curr_case.idf, ax)
        ax = plot_nodes(Gm, pos, ax)
        ax = plot_edges(Gm, pos, ax, median, cmap, (min_val, max_val))
        ax = set_axis_ticks(ax)
        drn = "NORTH_EAST" if windir else "NORTH_WEST"
        ax.set_title(f" {drn}")

    case_info, qoi_info = get_plot_labels(curr_case, qois[0], "AFN Net Flow Rate (1>2 - 2>1)", True)
    fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=qoi_info)
    fig.suptitle(f"{case_info}")

    return fig


def save_figures_for_all_cases():
    qoi1 = 'AFN Linkage Node 1 to Node 2 Volume Flow Rate'
    qoi12 = 'AFN Linkage Node 2 to Node 1 Volume Flow Rate'
    qois = [qoi1, qoi12]
    case_data = retrieve_cases()
    figures_root  = Path.cwd() / "figures" / "net_linkages"
    for sample_case in case_data:
        fig = create_data_on_network_fig_facet_winddir(case_data, sample_case, qois)
        fname = f"{sample_case.case_name}.png"
        figures_path = figures_root / fname
        fig.savefig(figures_path)
