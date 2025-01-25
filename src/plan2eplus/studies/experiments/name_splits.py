from typing import Callable
import polars as pl
import functools
from plan2eplus.helpers.variable_interfaces import all_variables as vars
from plan2eplus.studies.analysis2.all_cases_v_time import create_space_and_site_dfs
from plan2eplus.studies.experiments.retrieve import retrieve_comparison_groups
from plan2eplus.studies.setup.data_wrangle2 import (
    create_wide_dataframe_for_many_qois_and_cases,
)
from .retrieve import COMPARISON_GROUPS


def split_by_case_type_and_alias(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        case_type=pl.when(pl.col("case_names").str.contains("amb"))
        .then(pl.lit("A"))
        .when(pl.col("case_names").str.contains("bol"))
        .then(pl.lit("B"))
        .otherwise(pl.lit("C"))
    )


def split_by_materials(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        exp_type=pl.when(pl.col("case_names").str.contains("Light"))
        .then(pl.lit("Light"))
        .when(pl.col("case_names").str.contains("Medium"))
        .then(pl.lit("Medium"))
        .otherwise(pl.lit("Heavy"))
    )


def split_by_doors(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        exp_type=pl.when(pl.col("case_names").str.contains("CLOSED"))
        .then(pl.lit("CLOSED"))
        .when(pl.col("case_names").str.contains("DYNAMIC"))
        .then(pl.lit("DYNAMIC"))
        .otherwise(pl.lit("OPEN"))
    )


def split_by_windows(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        exp_type=pl.when(pl.col("case_names").str.contains("1.3"))
        .then(pl.lit("+30%"))
        .when(pl.col("case_names").str.contains("0.7"))
        .then(pl.lit("-30%"))
        .otherwise(pl.lit("Control"))
    )


def get_split_fx(
    comparison_group: COMPARISON_GROUPS,
) -> Callable[[pl.DataFrame], pl.DataFrame]:
    match comparison_group:
        case "doors":
            return split_by_doors
        case "windows":
            return split_by_windows
        case "materials":
            return split_by_materials
        case _:
            raise Exception("Invalid group ")


def get_chart_details(comparison_group: COMPARISON_GROUPS):
    match comparison_group:
        case "doors":
            return ("Door Status", ["OPEN", "DYNAMIC", "CLOSED"])
        case "windows":
            return ("Window Area", ["+30%", "Control", "-30%"])
        case "materials":
            return ("Material Type", ["Light", "Medium", "Heavy"])
        case _:
            raise Exception("Invalid group ")
        

def get_table_details(comparison_group: COMPARISON_GROUPS):
    match comparison_group:
        case "doors":
            control = "OPEN"
        case "windows":
            control = "Control"
        case "materials":
            control = "Medium"
        case _:
            raise Exception("Invalid group ")
    table_name = f"{comparison_group.title()} Experiment"
    return (control, table_name)


@functools.lru_cache
def create_and_split_data_by_exp(comparison_group: COMPARISON_GROUPS):
    # TODO => could this be created in a neater way?
    cases = retrieve_comparison_groups(comparison_group)
    df, _ = create_space_and_site_dfs(
        cases=cases,
        space_qois=[vars.afn.zone["vent_vol"], vars.afn.zone["mix_vol"]],
        site_qois=[vars.site.wind["speed"]],
    )
    df_temp = create_wide_dataframe_for_many_qois_and_cases(
        cases, [vars.zone.temp["zone_mean_air_temp"]]
    )
    df_vol = df.join(df_temp, on=["case_names", "space_names", "datetimes"])

    df_agg = df_vol.group_by("case_names").agg(
        [
            pl.mean("AFN Zone Ventilation Volume [m3]"),
            pl.mean("AFN Zone Mixing Volume [m3]"),
            pl.mean("Zone Mean Air Temperature [C]"),
        ]
    )
    df_split = split_by_case_type_and_alias(df_agg)
    split_fx = get_split_fx(comparison_group)
    return split_fx(df_split)
