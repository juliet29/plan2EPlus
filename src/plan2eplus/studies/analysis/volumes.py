from pathlib import Path
import seaborn as sns
import seaborn.objects as so
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from ..setup.data_wrangle import get_plot_labels

# from ..setup.materials_setup import *
from .dataframes import create_zone_vol_df_many
from ..setup.interfaces import CaseData
from ..setup.materials_setup import retrieve_cases
from ...helpers.dates import today


def get_save_details():
    FOLDER = f"{today}_medium_volumes"
    return Path.cwd() / "figures" / FOLDER


def init_df():
    cases = retrieve_cases()
    medium_cases = [i for i in cases if "Medium" in i.case_name]
    sc = medium_cases[0]
    df_vol = create_zone_vol_df_many(medium_cases)
    return df_vol, sc


def hist_and_ecdf_plots(
    df_vol: pl.DataFrame, sc: CaseData, values, qoi, is_saved=False
):
    sns.set_style("darkgrid")
    df_filter = df_vol.filter(pl.col(values) > 0)
    _, qoi_info = get_plot_labels(sc, df_vol[qoi][0])
    figures_root = get_save_details()

    def hist_plot():
        fig, ax = plt.subplots()
        g = sns.histplot(
            df_filter, x=values, hue="case_names", kde=True, multiple="stack", ax=ax
        )
        g.set_xlabel(qoi_info)
        if is_saved:
            fig.savefig(figures_root / f"dist_{qoi}")

    def ecdf_plot():
        fig, ax = plt.subplots()
        g = sns.ecdfplot(
            df_vol,
            x=values,
            hue="case_names",
            alpha=0.5,
            linewidth=5,
            linestyle="dotted",
            ax=ax,
        )
        g.set_xlabel(qoi_info)
        if is_saved:
            fig.savefig(figures_root / f"ecdf_{qoi}")

    hist_plot()
    ecdf_plot()


def aggregate_and_compare(df_vol: pl.DataFrame):
    df_vol2 = df_vol.with_columns(combined_vent=pl.col("values") + pl.col("values_0"))
    df_agg = df_vol2.group_by("case_names").agg(
        [
            pl.mean("values").alias("vent"),
            pl.mean("values_0").alias("mixing"),
            pl.mean("combined_vent"),
            pl.mean("values_1").alias("temp"),
        ]
    )
    return df_agg


def plot_combined_vent_vs_temp(df_vol: pl.DataFrame, is_saved=False):
    df_agg = aggregate_and_compare(df_vol)
    figures_root = get_save_details()
    g = (
        so.Plot(
            df_agg,
            x="temp",
            y="combined_vent",
            color="case_names",
        )
        .add(so.Dot(pointsize=20, marker="X"))
        .scale(color="flare")
    )  # type: ignore
    if is_saved:
        g.save(figures_root / f"vent_v_temp")
    return df_agg, g
