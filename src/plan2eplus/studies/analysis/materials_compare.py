from pathlib import Path
import seaborn as sns
import seaborn.objects as so
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from .volumes import aggregate_and_compare
from ..setup.data_wrangle import get_plot_labels

# from ..setup.materials_setup import *
from .dataframes import create_zone_vol_df_many
from ..setup.interfaces import CaseData
from ..setup.materials_setup import retrieve_cases


def get_save_details():
    FOLDER = "materials_compare"
    return Path.cwd() / "figures" / FOLDER


def init_df():
    cases = retrieve_cases()
    df_vol = create_zone_vol_df_many(cases)
    sc = cases[0]
    return df_vol, sc


def aggregate_and_compare_materials(df_vol):
    figures_root = get_save_details()
    df_agg = aggregate_and_compare(df_vol)
    df_agg2 = df_agg.with_columns(
        material_type=pl.when(pl.col("case_names").str.contains("Light"))
        .then(pl.lit("Light"))
        .when(pl.col("case_names").str.contains("Medium"))
        .then(pl.lit("Medium"))
        .otherwise(pl.lit("Heavy")),
        case_type=pl.when(pl.col("case_names").str.contains("amb"))
        .then(pl.lit("amb"))
        .when(pl.col("case_names").str.contains("bol"))
        .then(pl.lit("bol"))
        .otherwise(pl.lit("red")),
    )
    g = so.Plot(df_agg2, x="temp", y="combined_vent", color="case_type", marker="material_type").add(so.Dot(pointsize=15)).scale(color="flare").plot().save(figures_root / f"vent_v_temp")  # type: ignore
    g.show()
    return df_agg2, g
