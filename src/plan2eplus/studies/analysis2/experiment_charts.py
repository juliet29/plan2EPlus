import functools
import polars as pl
import altair as alt

from plan2eplus.helpers.variable_interfaces import all_variables as vars
from plan2eplus.helpers.dates import create_save_details
from plan2eplus.studies.analysis2.all_cases_v_time import create_space_and_site_dfs
from plan2eplus.studies.experiments.name_splits import (
    get_chart_details,
    split_by_case_type_and_alias,
    split_by_doors,
    split_by_materials,
    split_by_windows,
)
from plan2eplus.studies.experiments.scatter import get_split_fx
from plan2eplus.studies.setup.data_wrangle2 import (
    create_wide_dataframe_for_many_qois_and_cases,
)
from ..experiments.retrieve import COMPARISON_GROUPS, retrieve_comparison_groups


def get_save_details():
    return create_save_details("exp_res2")

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


def create_exp_chart(
    df: pl.DataFrame,
    comparison_group: COMPARISON_GROUPS,
    save_chart=False,
):
    df = create_and_split_data_by_exp(comparison_group)
    legend_title, sort_order = get_chart_details(comparison_group)
    base = (
        alt.Chart(df)
        .mark_point()
        .encode(color=alt.Color("exp_type").title(legend_title).sort(sort_order))
        .properties(width=100, height=150)
    )

    x_encoding = alt.X("case_type:N", title="Plan")
    y_encodings = [
        alt.Y(r"AFN Zone Ventilation Volume \[m3\]", title="Vent. Vol. [m³/s]"),
        alt.Y(r"AFN Zone Mixing Volume \[m3\]", title="Mixing Vol. [m³/s]"),
        alt.Y(r"Zone Mean Air Temperature \[C\]", title="Temp [ºC]"),
    ]

    chart = alt.hconcat()
    for y_encoding in y_encodings:
        chart |= base.encode(x=x_encoding, y=y_encoding.scale(zero=False))

    if save_chart:
        chart.save(get_save_details() / f"{comparison_group}.png", scale_factor=3)
    return chart


def save_charts_for_all_groups():
    for g in ['windows', 'materials', 'doors']:
        df = create_and_split_data_by_exp(g)
        create_exp_chart(df, g, save_chart=True)

