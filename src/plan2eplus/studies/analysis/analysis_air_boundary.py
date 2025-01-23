from ...helpers.variable_interfaces import all_variables
from ..setup.data_wrangle import create_dataframe_for_many_cases, join_any_data
from ..setup.interfaces import CaseData
from ..setup.setup import retrieve_case_data
import polars as pl


def get_qois():
    qoi1 = all_variables.afn.linkage["flow12"]
    qoi12 = all_variables.afn.linkage["flow21"]
    qoi2 = all_variables.afn.zone["ach"]
    qoi3 = all_variables.afn.zone["vent_vol"]
    qoi4 = all_variables.zone.temp["zone_mean_air_temp"]

    return qoi1, qoi12, qoi2, qoi3, qoi4


def get_df(case_data: CaseData):
    qois = get_qois()
    df = create_dataframe_for_many_cases([case_data], qois[0])
    return join_any_data(df, [case_data], qois[1])


def get_zone_df(case_data: CaseData):
    _, _, ach, vent_vol, *_ = get_qois()
    df = create_dataframe_for_many_cases([case_data], ach)
    return join_any_data(df, [case_data], vent_vol)


def get_airboundary_case():
    inputs_dir = "case_bol_5"
    outputs_dir = "tests/test23_airwall"
    return retrieve_case_data(inputs_dir, outputs_dir, "airwall")


def get_airboundary_with_surf_case():
    inputs_dir = "case_bol_5"
    outputs_dir = "tests/test25_airwall"
    return retrieve_case_data(inputs_dir, outputs_dir, "airwall_surf")


def get_no_door_case():
    inputs_dir = "case_bol_5"
    outputs_dir = "tests/test24_no_door"
    return retrieve_case_data(inputs_dir, outputs_dir, "no_door")


def get_normal_door_case():
    inputs_dir = "case_bol_5"
    outputs_dir = "oct_h4h_plans/case_bol_5"
    return retrieve_case_data(inputs_dir, outputs_dir, "just_door")


def create_data(df_select):
    dfs = [
        df_select(i)
        for i in [
            get_no_door_case(),
            get_airboundary_case(),
            get_airboundary_with_surf_case(),
            get_normal_door_case(),
        ]
    ]
    return pl.concat(dfs, how="vertical")


def get_df_many(case_data: list[CaseData]):
    qois = get_qois()
    df = create_dataframe_for_many_cases(case_data, qois[0])
    return join_any_data(df, case_data, qois[1])


def get_zone_df_many(case_data: list[CaseData]):
    _, _, ach, vent_vol, temp = get_qois()
    df = create_dataframe_for_many_cases(case_data, temp)
    return join_any_data(df, case_data, ach)
