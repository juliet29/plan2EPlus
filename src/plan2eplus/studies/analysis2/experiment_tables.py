from collections import defaultdict, namedtuple
from itertools import product

import polars as pl
from great_tables import GT

from plan2eplus.helpers.helpers import ContainsAsEqualsString, chain_flatten
from plan2eplus.studies.experiments.name_splits import create_and_split_data_by_exp, get_table_details
from plan2eplus.studies.experiments.retrieve import COMPARISON_GROUPS


short_qois = ["vent", "mix", "temp"]
stat_names = ["mean", "std", "max_diff"]
other_cols = ["_".join(i) for i in list(product(short_qois, stat_names))]
Stats = namedtuple("Stats", ["study_type", *other_cols])


def create_stats(df: pl.DataFrame, filter_exp: pl.Expr, exp_name: str):
    qois = [
        "AFN Zone Ventilation Volume [m3]",
        "AFN Zone Mixing Volume [m3]",
        "Zone Mean Air Temperature [C]",
    ]

    def get_stats(qoi):
        case = df.filter(filter_exp)[qoi]
        return [case.mean(), case.std(), case.max() - case.min()]

    all_stats = chain_flatten([get_stats(qoi) for qoi in qois])
    return Stats(exp_name, *all_stats)


def create_stats_df(df: pl.DataFrame, control_case_name: str):
    res = [
        create_stats(df, pl.col("exp_type") == control_case_name, "Across")._asdict(),
        create_stats(df, pl.col("case_type") == "A", "A")._asdict(),
        create_stats(df, pl.col("case_type") == "B", "B")._asdict(),
        create_stats(df, pl.col("case_type") == "C", "C")._asdict(),
    ]
    # smush the lists together..
    dd = defaultdict(list)
    for d in res:
        for key, value in d.items():
            dd[key].append(value)
    return pl.DataFrame(dd)


def rename_table_columns(i: str) -> str:
    cstring = ContainsAsEqualsString(i)
    match cstring:
        case "mean":
            return "Mean"
        case "std":
            return "Std."
        case "max_diff":
            return "Max. Diff."
        case _:
            return i


def create_table(df: pl.DataFrame, comparison_group: COMPARISON_GROUPS):
    control_case_name, title = get_table_details(comparison_group)
    stats_df = create_stats_df(df, control_case_name)
    return (
        GT(stats_df)
        .tab_header(title=title)
        # .tab_stub(rowname_col="study_type")
        .tab_spanner(label="Vent. Vol. [m³]", columns=other_cols[0:3])
        .tab_spanner(
            label="Mixing Vol. [m³]",
            columns=other_cols[3:6],
        )
        .tab_spanner(label="Temp. [ºC]", columns=other_cols[6:])
        .fmt_number(
            columns=pl.selectors.numeric(),
            n_sigfig=2,
        )  # or decimals..
        .cols_label({i: rename_table_columns(i) for i in other_cols})
    )

def print_latex_for_all_tables():
    for g in ["windows", "materials", "doors"]:
        df = create_and_split_data_by_exp(g)
        tbl = create_table(df, g)
        print(tbl.as_latex())
        print("\n \n \n")
