from pathlib import Path
from typing import get_args
import polars as pl
import seaborn.objects as so
import functools

from ...helpers.variable_interfaces import all_variables as vars
from .retrieve import retrieve_comparison_groups, COMPARISON_GROUPS
from ..analysis2.all_cases_v_time import create_space_and_site_dfs
from ..setup.data_wrangle2 import create_wide_dataframe_for_many_qois_and_cases
from .name_splits import (
    get_split_fx,
    split_by_doors,
    split_by_materials,
    split_by_case_type,
    split_by_windows,
)
from ...helpers.dates import today, create_save_details


CURR_EXP_GROUP = "241120_summer"


def get_save_details():
    FOLDER = f"{today}_comparison"
    path = Path.cwd() / "figures" / FOLDER
    if not path.exists():
        path.mkdir()
    return path


# TODO convert
# def get_save_details(comparison):
#     return create_save_details(comparison)


@functools.lru_cache
def create_comparison_df(comparison_group: COMPARISON_GROUPS):
    cases = retrieve_comparison_groups(comparison_group, CURR_EXP_GROUP)

    df_temp = create_wide_dataframe_for_many_qois_and_cases(
        cases, [vars.zone.temp["zone_mean_air_temp"]]
    )

    # TODO doesnt need to be space and site
    df, _ = create_space_and_site_dfs(
        cases=cases,
        space_qois=[vars.afn.zone["vent_vol"], vars.afn.zone["mix_vol"]],
        site_qois=[vars.site.wind["speed"]],
    )

    df_vol = df.join(
        df_temp, on=["case_names", "space_names", "datetimes"]
    ).with_columns(
        combined_vent=pl.col("AFN Zone Ventilation Volume [m3]")
        + pl.col("AFN Zone Mixing Volume [m3]")
    )
    df_vol.head()

    df_agg = df_vol.group_by("case_names").agg(
        [
            pl.mean("AFN Zone Ventilation Volume [m3]"),
            pl.mean("AFN Zone Mixing Volume [m3]"),
            pl.mean("Zone Mean Air Temperature [C]"),
        ]
    )

    split_fx = get_split_fx(comparison_group)
    return split_fx(split_by_case_type(df_agg))


def scatter_plot(
    df_agg: pl.DataFrame,
    comparison_group: COMPARISON_GROUPS,
    qoi: str,
    qoi_name: str,
    is_saved: bool,
):
    figures_root = get_save_details()
    g = so.Plot(df_agg, x="Zone Mean Air Temperature [C]", y=qoi, color="case_type", marker="exp_type").add(so.Dot(pointsize=15)).scale(color="flare").plot()  # type: ignore
    g.show()
    if is_saved:
        g.save(figures_root / f"{comparison_group}_{qoi_name}", bbox_inches="tight")
    return g


def create_plots_for_comparison_group(
    comparison_group: COMPARISON_GROUPS, is_saved=False
):
    df_agg = create_comparison_df(comparison_group)
    qois = ["AFN Zone Ventilation Volume [m3]", "AFN Zone Mixing Volume [m3]"]
    qoi_names = ["vent", "mixing"]

    return [
        scatter_plot(df_agg, comparison_group, i, i_name, is_saved)
        for i, i_name in zip(qois, qoi_names)
    ]


def save_plots_for_all_experiments():
    for cgroup in get_args(COMPARISON_GROUPS):
        r = create_plots_for_comparison_group(cgroup, is_saved=True)
