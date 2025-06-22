from copy import deepcopy
import polars as pl
from ladybug.datacollection import BaseCollection

from plan2eplus.helpers.helpers import extend_data
from plan2eplus.helpers.read_sql import get_name_for_spatial_data

from ...helpers.read_sql import create_collections_for_variable

# from .plots import get_name_for_spatial_data
from .setup import CaseData
from .interfaces import DataDescription, InitData, SQLiteResult


# TODO way to get this data for just one item..
def get_dataset_description(dataset: BaseCollection):
    qoi = dataset.header.metadata["type"]
    unit = dataset.header.unit
    analysis_period = str(dataset.header.analysis_period)  # what if tehre are two?
    spatial_data = get_name_for_spatial_data(dataset)
    return DataDescription(qoi, unit, analysis_period, spatial_data)


def create_init_data(case_name, dataset):
    dd = get_dataset_description(dataset)
    qoi_w_unit = f"{dd.qoi} [{dd.unit}]"
    return InitData(case_name, dd.space, dataset.values, dataset.datetimes, qoi_w_unit)


def create_long_dataframe(data: InitData):
    len_data = len(data.values)
    return pl.DataFrame(
        {
            "case_names": extend_data(data.case_name, len_data),
            "space_names": extend_data(data.space, len_data),
            "datetimes": data.datetimes,
            "qoi": extend_data(data.qoi, len_data),
            "values": data.values,
        }
    )


def create_long_dataframe_with_qoi(data: InitData):
    len_data = len(data.values)
    return pl.DataFrame(
        {
            "case_names": extend_data(data.case_name, len_data),
            "space_names": extend_data(data.space, len_data),
            "datetimes": data.datetimes,
            "qoi": extend_data(data.qoi, len_data),
            "values": data.values,
        }
    )


def create_dataframe_for_case(case_name: str, sql: SQLiteResult, qoi: str):
    collection = create_collections_for_variable(sql, qoi)
    init_data = [create_init_data(case_name, i) for i in collection]
    dataframes = [create_long_dataframe(i) for i in init_data]
    return pl.concat(dataframes, how="vertical")


def create_dataframe_for_many_cases(cases: list[CaseData], qoi: str):
    dataframes = [create_dataframe_for_case(i.case_name, i.sql, qoi) for i in cases]
    return pl.concat(dataframes, how="vertical")


def create_site_var(case: CaseData, qoi: str):
    assert "site" in qoi.lower()
    dataset = create_collections_for_variable(case.sql, qoi)[0]
    dd = get_dataset_description(dataset)
    return InitData(case.case_name, dd.space, dataset.values, dataset.datetimes, dd.qoi)


def join_site_data(df: pl.DataFrame, case: CaseData, qoi: str, ix=0):
    data = create_site_var(case, qoi)
    cases = df["case_names"].unique()
    len_data = len(data.values)

    def create_case_df(case_name):
        return pl.DataFrame(
            {
                "case_names": extend_data(case_name, len_data),
                "datetimes": data.datetimes,
                "qoi": extend_data(data.qoi, len_data),
                "values": data.values,
            }
        )

    dfs = [create_case_df(i) for i in cases]
    site_df_for_cases = pl.concat(dfs, how="vertical")
    joined_df = df.join(site_df_for_cases, on=["case_names", "datetimes"])
    return joined_df.rename({"qoi_right": f"qoi_{ix}", "values_right": f"values_{ix}"})


def join_any_data(df: pl.DataFrame, cases: list[CaseData], qoi: str, ix=0):
    # TODO check for that the cases are the same,
    # and the df has the right schema.. ~ df.shema ///
    # also check that not repeating qoi
    # and that space names are the same..
    dataframes = [create_dataframe_for_case(i.case_name, i.sql, qoi) for i in cases]
    df_for_all_cases = pl.concat(dataframes, how="vertical")

    joined_df = df.join(df_for_all_cases, on=["case_names", "datetimes", "space_names"])

    return joined_df.rename({"qoi_right": f"qoi_{ix}", "values_right": f"values_{ix}"})


### TODO move to plots..


def get_plot_labels(case: CaseData, qoi: str, custom_qoi=None, ap=False):
    collection = create_collections_for_variable(case.sql, qoi)
    dd = get_dataset_description(collection[0])
    case_info = (
        f"Case: {case.case_name}"
        if not ap
        else f"Case: {case.case_name}. AP: {dd.analysis_period}"
    )
    # <br><sup> {dd.analysis_period} </sup>

    qoi_name = custom_qoi if custom_qoi else dd.qoi
    qoi_info = f"{qoi_name} [{dd.unit}]"
    return case_info, qoi_info


def add_displot_labels(g, case: CaseData, qoi: str):
    case_info, qoi_info = get_plot_labels(case, qoi)
    g.set_xlabels(qoi_info)
    g.figure.suptitle(case_info)
    return g


# qoi1 = 'AFN Linkage Node 1 to Node 2 Volume Flow Rate'
# qoi2 = "Site Wind Speed"
# qoi3 = "Site Wind Direction"
# qoi4 = all_variables.afn.zone["ach"]
# qoi4

# case_data = retrieve_cases()
# sample_case = case_data[0]
# df = create_dataframe_for_all_cases(case_data, qoi4)
# df.head()

# df = create_dataframe_for_case(case_name, sql, curr_qoi)
# df_vals = df.filter(pl.col("values") > 0 )


# filtering data based on wind direction .

# df2 = join_site_data(sample_case, qoi3, df)
# df2.head()
# df3 = df2.with_columns(
#     pl.when(pl.col("values_right") > 100)
#     .then(1)
#     .otherwise(0)
#     .alias("wind_dir")
# )
# df3.head(2)

# g = sns.FacetGrid(df3, col="wind_dir")
# g.map(sns.boxplot, "case_names", "values", order=["amb_b1", "bol_5","red_b1"])


# g = sns.displot(df, x="values", hue="space_names", kind="kde")
# g = add_displot_labels(g, sample_case, curr_qoi)
