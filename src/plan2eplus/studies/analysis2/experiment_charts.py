import polars as pl
import altair as alt

from plan2eplus.helpers.dates import create_save_details
from plan2eplus.studies.experiments.name_splits import (
    get_chart_details,
)
from plan2eplus.studies.experiments.name_splits import create_and_split_data_by_exp
from ..experiments.retrieve import COMPARISON_GROUPS


def get_save_details():
    return create_save_details("exp_res2_shapes")


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
        .encode(
            # color=alt.Color("exp_type").title(legend_title).sort(sort_order).legend(None),
            shape=alt.Shape("exp_type").title(legend_title).sort(sort_order),
            # detail=alt.Detail("exp_type:N").title(legend_title),
        )
        .properties(width=100, height=150)
    )

    x_encoding = alt.X("case_type:N", title="Plan")
    y_encodings = [
        alt.Y(r"AFN Zone Ventilation Volume \[m3\]", title="Vent. Vol. [m³]"),
        alt.Y(r"AFN Zone Mixing Volume \[m3\]", title="Mixing Vol. [m³]"),
        alt.Y(r"Zone Mean Air Temperature \[C\]", title="Temp [ºC]"),
    ]

    chart = alt.hconcat()
    for y_encoding in y_encodings:
        chart |= base.encode(x=x_encoding, y=y_encoding.scale(zero=False))

    if save_chart:
        chart.save(get_save_details() / f"{comparison_group}.png", scale_factor=3)
    return chart


def save_charts_for_all_groups():
    for g in ["windows", "materials", "doors"]:
        df = create_and_split_data_by_exp(g)
        create_exp_chart(df, g, save_chart=True)
