from pathlib import Path
from geomeppy import IDF
import polars as pl
from analysis.helpers import convert_zone_space_name
from network.network import create_base_graph, get_node_partners
from plan.helpers import create_room_map
from setup.interfaces import CaseData
from helpers.variable_interfaces import all_variables
from setup.data_wrangle import (
    create_dataframe_for_many_cases,
    join_any_data,
    create_dataframe_for_case,
    join_site_data,
)


def create_zone_vol_df_many(case_data: list[CaseData]):
    vent_vol = all_variables.afn.zone["vent_vol"]
    mix_vol = all_variables.afn.zone["mix_vol"]
    temp = all_variables.zone.temp["zone_mean_air_temp"]

    df = create_dataframe_for_many_cases(case_data, vent_vol)
    df2 = join_any_data(df, case_data, mix_vol)
    return join_any_data(df2, case_data, temp, 1)


def create_zone_rate_df(case: CaseData):
    zq = all_variables.afn.zone
    qois = [
        zq["vent_heat_gain"],
        zq["vent_heat_loss"],
        zq["mix_heat_gain"],
        zq["mix_heat_loss"],
    ]

    dfs = [create_dataframe_for_case(case.case_name, case.sql, qoi) for qoi in qois]
    return pl.concat(dfs, how="vertical")


def create_site_df(case: CaseData):
    sq = all_variables.site
    qois = [
        sq.temp["db"],
        sq.solar["direct_rad"],
        sq.wind["speed"],
        sq.wind["direction"],
    ]

    dfs = [create_dataframe_for_case(case.case_name, case.sql, qoi) for qoi in qois]
    return pl.concat(dfs, how="vertical")


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


def map_linkage_names_to_G(idf: IDF, path_to_input: Path, df: pl.DataFrame):
    G, _ = create_base_graph(idf, path_to_input)
    fx = lambda surf_name: get_node_partners(idf, G, surf_name)
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


def create_linkage_df(case: CaseData) -> pl.DataFrame:
    av = all_variables.afn
    qois = [
        av.linkage["flow12"],
        av.linkage["flow21"],
    ]
    df = create_dataframe_for_case(case.case_name, case.sql, qois[0])
    df = join_any_data(df, [case], qois[1])
    df = df.with_columns(net_linkage=pl.col("values") - pl.col("values_0"))

    df = map_linkage_names_to_G(case.idf, case.path_to_input, df)

    def flip_edge(e):
        return [e[1], e[0]]

    flipped_edges = [
        flip_edge(e) if v < 0 else e
        for e, v in zip(df["room_pairs"], df["net_linkage"])
    ]
    df = df.hstack([pl.Series("directed_pairs", flipped_edges)])
    # )
    return df