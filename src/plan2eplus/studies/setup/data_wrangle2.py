import polars as pl

from ...helpers.helpers import extend_data

from ...helpers.read_sql import create_collections_for_variable
from .data_wrangle import create_init_data
from .interfaces import InitData, CaseData
from copy import deepcopy


def create_long_dataframe(data: InitData):
    len_data = len(data.values)
    return pl.DataFrame(
        {
            "case_names": extend_data(data.case_name, len_data),
            "space_names": extend_data(data.space, len_data),
            "datetimes": data.datetimes,
            data.qoi: data.values,
        }
    )


def create_dataframe_for_case(case: CaseData, qoi: str):
    collection = create_collections_for_variable(case.sql, qoi)
    init_data = [create_init_data(case.case_name, i) for i in collection]
    dataframes = [create_long_dataframe(i) for i in init_data]
    return pl.concat(dataframes, how="vertical")


# TODO ^ the above is duplicated in graphbem for now, but dont want to break network graphs 6/21/25


def create_wide_dataframe_for_many_qois(case: CaseData, qois: list[str]):
    dfs = [create_dataframe_for_case(case, qoi) for qoi in qois]
    join_df = dfs[0]
    for qoi, df in zip(qois[1:], dfs[1:]):
        assert set(join_df["space_names"]) == set(df["space_names"]), (
            f"{qoi} does not have the same space_names as others in dataframe"
        )
        join_df = join_df.join(df, on=["datetimes", "case_names", "space_names"])

    return join_df


def add_site_qois_wide(df: pl.DataFrame, case: CaseData, qois: list[str]):
    site_df = create_wide_dataframe_for_many_qois(case, qois)
    site_df = site_df.drop("space_names")
    temp_dfs = []
    for name in df["space_names"].unique():
        s = deepcopy(site_df)
        s.insert_column(-1, pl.Series(f"space_names", [name] * 96))
        temp_dfs.append(s)

    long_site_df = pl.concat(temp_dfs)
    assert long_site_df.shape[0] == df.shape[0]
    assert set(long_site_df["datetimes"]) == set(df["datetimes"])

    return df.join(
        long_site_df,
        on=["datetimes", "space_names", "case_names"],
    )


def create_wide_dataframe_for_many_qois_and_cases(
    cases: list[CaseData], qois: list[str]
):
    dfs = [create_wide_dataframe_for_many_qois(case, qois) for case in cases]
    return pl.concat(dfs, how="vertical")


# can i create a long df from a wide one with polars.. yes! using pivot... see cp work..
