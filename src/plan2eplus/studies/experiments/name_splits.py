from typing import Callable
import polars as pl

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


def get_split_fx(comparison_group: COMPARISON_GROUPS) -> Callable[[pl.DataFrame], pl.DataFrame]:
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
