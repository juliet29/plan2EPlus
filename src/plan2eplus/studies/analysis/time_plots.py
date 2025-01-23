import seaborn as sns

from .plot_helpers import set_axis_ticks
from 2.all_cases_v_time import create_space_and_site_dfs
from experiments.retrieve import retrieve_control_cases
from ..setup.data_wrangle2 import (
    create_wide_dataframe_for_many_qois,
    create_wide_dataframe_for_many_qois_and_cases,
)
from .helpers import extract_times


def site_and_qoi_plot(df_site, df, qoi_site, qoi_site_label, qoi_zone):
    sns.lineplot(
        data=df_site,
        y="Site Outdoor Air Drybulb Temperature [C]",
        x="time",
        color="black",
        linewidth=2,
        label="Outdoor Drybulb Temp",
    )
    g = sns.lineplot(
        df, x="time", y="Zone Mean Air Temperature [C]", hue="case_names", errorbar=None
    )
    set_axis_ticks(g)

    g.set_ylabel("Temperature [ºC]")
    g.set_xlabel("Time")


def boxplot(df, qoi_zone):
    sns.boxplot(data=df, x="case_names", y=qoi_zone, hue="case_names")


# def temperature_dfs():
#     cases = retrieve_control_cases()
#     df = create_wide_dataframe_for_many_qois_and_cases(cases, [vars.zone.temp["zone_mean_air_temp"]])
#     df = extract_times(df)

#     df_site = create_wide_dataframe_for_many_qois(cases[0], [vars.site.temp["db"], vars.site.solar["direct_rad"]])
#     df_site = extract_times(df_site)


def vent_dfs():
    cases = retrieve_control_cases()
    df, df_site = create_space_and_site_dfs(
        cases=cases,
        space_qois=[vars.afn.zone["vent_vol"], vars.afn.zone["mix_vol"]],
        site_qois=[vars.site.wind["speed"]],
    )
