from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from .dataframes import (
    create_linkage_df,
    create_pressure_df,
)
from .helpers import get_min_max, normalize_column
from .plot_helpers import (
    create_colorbar,
    plot_nodes,
    plot_zone_domains,
    plot_edges_widths,
    set_axis_ticks,
)
from .plot_subsurfaces import plot_surfaces
from ..setup.interfaces import CaseData
from ..network.network import init_multigraph


def get_room_values(case: CaseData, time: datetime):
    df = create_pressure_df(case)
    dft = df.filter(
        (pl.col("qoi").str.contains("Total Pressure"))
        & (pl.col("is_ext") == False)
        & (pl.col("datetimes") == time)
    )
    res = dft.select("room_names", "values")
    return res


def get_linkage_values(case: CaseData, time: datetime):
    df = create_linkage_df(case)
    dft = df.filter((pl.col("datetimes") == time))
    res = dft.select("directed_pairs", "net_linkage")

    return res


def add_nodes(case: CaseData, Gm, pos, fig, ax, time: datetime):
    cmap = sns.color_palette("YlOrBr", as_cmap=True)
    res = get_room_values(case, time)
    min_max = get_min_max(res, "values")
    ax = plot_nodes(Gm, pos, ax, res["room_names"], res["values"], cmap, min_max)
    fig = create_colorbar(fig, ax, cmap, min_max, "Total Pressure")
    return fig, ax


def add_edges(case: CaseData, Gm, pos, fig, ax, time: datetime):
    res = get_linkage_values(case, time)
    edge_widths = normalize_column(res, "net_linkage", range=(1, 4))
    ax = plot_edges_widths(Gm, pos, ax, res["directed_pairs"], edge_widths)
    # ax = plot_edge_labels(Gm, pos, ax, res["directed_pairs"], res["net_linkage"])
    return fig, ax


# @functools.lru_cache
def create_network_plot(case: CaseData, hour_min=(12, 0)):
    time = datetime(2017, 7, 1, *hour_min)
    Gm, pos = init_multigraph(case.idf, case.path_to_input)
    fig, ax = plt.subplots(nrows=1, figsize=(8, 6))
    ax = plot_zone_domains(case.idf, ax)
    fig, ax = add_nodes(case, Gm, pos, fig, ax, time)
    ax, data = plot_surfaces(case, time, ax)
    fig, ax = add_edges(case, Gm, pos, fig, ax, time)
    ax = set_axis_ticks(ax)

    stime = time.strftime("%H:%M")
    fig.suptitle(f"{case.case_name} @ {stime}")
    return fig, ax


def name_mapper(name):
    match name:
        case "amb_b1_Medium":
            return "A"
        case "bol_5_Medium":
            return "B"
        case "red_b1_Medium":
            return "C"


def create_network_subplot(case: CaseData, fig, ax, hour_min=(12, 0)):
    time = datetime(2017, 7, 1, *hour_min)
    Gm, pos = init_multigraph(case.idf, case.path_to_input)
    # fig, ax = plt.subplots(nrows=1, figsize=(8, 6))
    ax = plot_zone_domains(case.idf, ax)
    fig, ax = add_nodes(case, Gm, pos, fig, ax, time)
    ax, data = plot_surfaces(case, time, ax)
    fig, ax = add_edges(case, Gm, pos, fig, ax, time)
    ax = set_axis_ticks(ax)

    stime = time.strftime("%H:%M")
    # fig.suptitle(f"{case.case_name} @ {stime}")
    ax.set_title(name_mapper(case.case_name))
    print(f"Time studied is: {stime}")
    return fig, ax


def get_save_details():
    FOLDER = "network_medium"
    return Path.cwd() / "figures" / FOLDER


def network_plots_for_many_cases(cases: list[CaseData], hour_min=(12, 0)):
    hour, min = hour_min
    time = f"{hour}_{min}"
    figures_root = get_save_details()
    for case in cases:
        fig = create_network_plot(case, hour_min)
        fig.savefig(figures_root / f"{case.case_name}_{time}")


def save_subplot(fig):
    figures_root = get_save_details()
    fig.savefig(figures_root / "subplot_save", dpi=300,  bbox_inches='tight')
