from pathlib import Path
from geomeppy import IDF
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

from analysis.helpers import convert_zone_space_name, get_min_max_values
from analysis.plot_helpers import create_colorbar, plot_nodes, plot_zone_domains
from plan.helpers import create_room_map
from setup.interfaces import CaseData
from helpers.variable_interfaces import all_variables
from setup.data_wrangle import create_dataframe_for_case, join_any_data
from network.network import get_partners_of_surface_or_subsurface, init_multigraph


def link_dfs_for_qois(case: CaseData, qois: list[str]):
    df = [create_dataframe_for_case(case.case_name, case.sql, qoi) for qoi in qois]
    return pl.concat(df, how="vertical")


def extract_times(df: pl.DataFrame):
    return df.with_columns(time=pl.col("datetimes").dt.to_string("%H:%M"))


def map_zone_names(path_to_input: Path, df: pl.DataFrame):
    room_map = create_room_map(path_to_input)
    fx = lambda name: convert_zone_space_name(room_map, name)
    return df.with_columns(
        room_names=pl.col("space_names").map_elements(fx, return_dtype=pl.String),
    )


def map_linkage_names(idf: IDF, df: pl.DataFrame):
    fx = lambda surf_name: get_partners_of_surface_or_subsurface(idf, surf_name)
    return df.with_columns(
        room_pairs=pl.col("space_names").map_elements(fx, return_dtype=pl.Object)
    )


### above are df helpers.. ^


def create_pressure_df(case: CaseData):
    av = all_variables.afn
    qois = [av.node["total_pressure"], av.node["wind_pressure"], av.node["temp"]]

    df = link_dfs_for_qois(case, qois)
    df = extract_times(df)
    df = map_zone_names(case.path_to_input, df)
    df = df.with_columns(
        is_ext=pl.when(pl.col("room_names").str.contains("ExtNode"))
        .then(True)
        .otherwise(False)
    )
    return df


def create_linkage_df_long(case: CaseData):
    av = all_variables.afn
    qois = [
        av.linkage["flow12"],
        av.linkage["flow21"],
    ]
    return link_dfs_for_qois(case, qois)


def create_linkage_df(case: CaseData):
    av = all_variables.afn
    qois = [
        av.linkage["flow12"],
        av.linkage["flow21"],
    ]
    df = create_dataframe_for_case(case.case_name, case.sql, qois[0])
    df = join_any_data(df, [case], qois[1])
    df = df.with_columns(net_linkage=pl.col("values") - pl.col("values_0"))
    df = map_linkage_names(case.idf, df)
    return df

### above goes to another file... ^

def get_room_values(case: CaseData, time=pl.datetime(2017, 7, 1, 12)):
    df = create_pressure_df(case)
    dft = df.filter(
        (pl.col("qoi").str.contains("Total Pressure"))
        & (pl.col("is_ext") == False)
        & (pl.col("datetimes") == time)
    )
    res = dft.select("room_names", "values")

    return res


def add_nodes(case: CaseData, Gm, pos, fig, ax):
    cmap = sns.light_palette("seagreen", as_cmap=True)
    res = get_room_values(case)
    min_max = get_min_max_values(res, "values")

    ax = plot_nodes(Gm, pos, ax, res["room_names"], res["values"], cmap, min_max)
    fig = create_colorbar(fig, ax, cmap, min_max, "Total Pressure")
    return fig, ax


def create_network_plot(case: CaseData):
    Gm, pos = init_multigraph(case.idf, case.path_to_input)
    fig, ax = plt.subplots(nrows=1)
    ax = plot_zone_domains(case.idf, ax)
    fig, ax = add_nodes(case, Gm, pos, fig, ax)

    fig.suptitle(f"{case.case_name}")
    return fig
