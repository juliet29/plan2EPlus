import polars as pl
import polars.selectors as cs
from ..setup.interfaces import CaseData
from ..setup.materials_setup import retrieve_cases
from ..setup.data_wrangle2 import (
    create_wide_dataframe_for_many_qois,
    add_site_qois_wide,
)
from .helpers import map_zone_names, extract_times, map_linkage_names_to_G
from ...helpers.variable_interfaces import all_variables as vars


def get_redwood_case():
    cases = retrieve_cases()
    medium_cases = [i for i in cases if "Medium" in i.case_name]
    [case] = [i for i in medium_cases if "red" in i.case_name]
    return case


# # TODO zone temp data..
# def get_col_regex(name):
#     return pl.col(f"^{name}.*$")


def create_linkage_df(case: CaseData) -> pl.DataFrame:
    av = vars.afn
    qois = [
        av.linkage["flow12"],
        av.linkage["flow21"],
    ]
    df = create_wide_dataframe_for_many_qois(case, qois)
    df = df.with_columns(
        net_linkage=(cs.contains(qois[0]) - cs.contains(qois[1]))
    )  # TODO check this calculation may be wrong

    df = map_linkage_names_to_G(case.idf, case.path_to_input, df)

    def flip_edge(e):
        return [e[1], e[0]]

    directed_pairs = [
        flip_edge(e) if v < 0 else e
        for e, v in zip(df["room_pairs"], df["net_linkage"])
    ]
    df = df.hstack([pl.Series("directed_pairs", directed_pairs)])
    return df


def get_external_node_df(case: CaseData):
    df = create_wide_dataframe_for_many_qois(case, [vars.afn.node["wind_pressure"]])
    return add_site_qois_wide(
        df, case, [vars.site.wind["speed"], vars.site.wind["direction"]]
    )


# def create_vol_df_for_many_cases():
