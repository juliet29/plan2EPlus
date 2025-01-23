from typing import NamedTuple
from pathlib import Path

import seaborn as sns
import matplotlib.pyplot as plt

from ...helpers.variable_interfaces import all_variables as vars
from ..analysis.helpers import extract_times
from ..analysis.plot_helpers import set_axis_ticks
from ..setup.data_wrangle2 import (
    create_wide_dataframe_for_many_qois,
    create_wide_dataframe_for_many_qois_and_cases,
)
from ..setup.interfaces import InitData, CaseData
from ...helpers.dates import today, create_save_details


# def get_save_details():
#     FOLDER  = f"{today}_control_case_compare"
#     return Path.cwd() / "figures" / FOLDER


def get_save_details():
    return create_save_details("control_case_compare")


# TODO move to dataframes..
def create_space_and_site_dfs(
    cases: list[CaseData], space_qois: list[str], site_qois: list[str]
):
    df = create_wide_dataframe_for_many_qois_and_cases(cases, space_qois)
    df = extract_times(df)

    df_site = create_wide_dataframe_for_many_qois(cases[0], site_qois)
    df_site = extract_times(df_site)

    return df, df_site


def get_temp_dfs(cases: list[CaseData]):
    df, df_site = create_space_and_site_dfs(
        cases,
        space_qois=[vars.zone.temp["zone_mean_air_temp"]],
        site_qois=[vars.site.temp["db"], vars.site.solar["direct_rad"]],
    )
    df = extract_times(df)

    return df, df_site


def get_ventilation_and_wind_speed_dfs(cases: list[CaseData]):
    df, df_site = create_space_and_site_dfs(
        cases=cases,
        space_qois=[vars.afn.zone["vent_vol"], vars.afn.zone["mix_vol"]],
        site_qois=[vars.site.wind["speed"]],
    )
    df = extract_times(df)
    return df, df_site


class QOIGroup(NamedTuple):
    site: str
    site_label: str
    zone: str


qoi_groups = {
    "temp": QOIGroup(
        "Site Outdoor Air Drybulb Temperature [C]",
        "Outdoor Drybulb Temp",
        "Zone Mean Air Temperature [C]",
    ),
    "vent": QOIGroup(
        "Site Wind Speed [m/s]", "Wind Speed", "AFN Zone Ventilation Volume [m3]"
    ),
    "mix": QOIGroup(
        "Site Wind Speed [m/s]", "Wind Speed", "AFN Zone Mixing Volume [m3]"
    ),
}


def site_and_qoi_plot(df, df_site, qoi_group: QOIGroup, is_saved=False):
    f, ax = plt.subplots()
    sns.lineplot(
        data=df_site,
        y=qoi_group.site,
        x="time",
        color="black",
        linewidth=2,
        label=qoi_group.site_label,
        ax=ax,
    )

    g = sns.lineplot(
        df, x="time", y=qoi_group.zone, hue="case_names", errorbar=None, ax=ax
    )
    set_axis_ticks(g)

    # g.set_ylabel("Temperature [ºC]")
    g.set_xlabel("Time")
    if is_saved:
        figures_root = get_save_details()
        f.savefig(figures_root / f"{qoi_group.zone}_line")

    return g


def site_and_qoi_plot_two_ax(df, df_site, qoi_group: QOIGroup, is_saved=False):
    f, ax = plt.subplots()
    g = sns.lineplot(
        df, x="time", y=qoi_group.zone, hue="case_names", errorbar=None, ax=ax
    )

    ax2 = g.twinx()

    sns.lineplot(data=df_site, y=qoi_group.site, x="time", color="black", linewidth=2, label=qoi_group.site_label, ax=ax2)  # type: ignore

    set_axis_ticks(g)

    # g.set_ylabel("Temperature [ºC]")
    g.set_xlabel("Time")
    g.grid(visible=False)
    if is_saved:
        figures_root = get_save_details()
        f.savefig(figures_root / f"{qoi_group.zone}_line")
    return g


def boxplot(df, qoi_group: QOIGroup, is_saved=False):
    f, ax = plt.subplots()
    g = sns.boxplot(data=df, x="case_names", y=qoi_group.zone, hue="case_names", ax=ax)
    if is_saved:
        figures_root = get_save_details()
        f.savefig(figures_root / f"{qoi_group.zone}_box")


def temp_plots(cases: list[CaseData], is_saved=False):
    df, df_site = get_temp_dfs(cases)
    qoi_group = qoi_groups["temp"]
    g1 = site_and_qoi_plot(df, df_site, qoi_group, is_saved)
    g2 = boxplot(df, qoi_group, is_saved)

    return g1, g2

    # TODO add tight layout when save..


def vent_plots(cases: list[CaseData], is_saved=False):
    df, df_site = get_ventilation_and_wind_speed_dfs(cases)
    qoi_group = qoi_groups["vent"]
    g1 = site_and_qoi_plot_two_ax(df, df_site, qoi_group, is_saved)
    g2 = boxplot(df, qoi_group, is_saved)

    return g1, g2


def mix_plots(cases: list[CaseData], is_saved=False):
    df, df_site = get_ventilation_and_wind_speed_dfs(cases)
    qoi_group = qoi_groups["mix"]
    g1 = site_and_qoi_plot_two_ax(df, df_site, qoi_group, is_saved)
    g2 = boxplot(df, qoi_group, is_saved)

    return g1, g2


def save_plots_to_compare_cases(cases):
    temp_plots(cases, True)
    vent_plots(cases, True)
    mix_plots(cases, True)
