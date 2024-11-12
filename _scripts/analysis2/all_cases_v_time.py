import seaborn as sns


from analysis.helpers import extract_times
from analysis.plot_helpers import set_axis_ticks
from setup.data_wrangle2 import (
    create_wide_dataframe_for_many_qois,
    create_wide_dataframe_for_many_qois_and_cases,
)
from setup.interfaces import InitData, CaseData


def create_space_and_site_dfs(
    cases: list[CaseData], space_qois: list[str], site_qois: list[str]
):
    df = create_wide_dataframe_for_many_qois_and_cases(cases, space_qois)
    df = extract_times(df)

    df_site = create_wide_dataframe_for_many_qois(cases[0], site_qois)
    df_site = extract_times(df_site)

    return df, df_site


def get_temp_plot(cases: list[CaseData]):
    df, df_site = create_space_and_site_dfs(
        cases,
        space_qois=[vars.zone.temp["zone_mean_air_temp"]],
        site_qois=[vars.site.temp["db"], vars.site.solar["direct_rad"]],
    )

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

    return g


def get_ventilation_and_speed_plot():
    pass