from copy import deepcopy
import polars as pl
from ladybug.datacollection import BaseCollection

from helpers.read_sql import get_collection_for_variable
from setup.plots import get_name_for_spatial_data
from setup.setup import CaseData
from setup.interfaces import DataDescription, InitData


def get_name_for_spatial_data(dataset: BaseCollection):
    keys = dataset.header.metadata.keys()
    for i in ["System", "Zone", "Surface"]:
        if i in keys:
            return dataset.header.metadata[i]
    else:
        raise Exception("Spatial type is not defined")
    
# TODO way to get this data for just one item.. 
def get_dataset_description(dataset: BaseCollection):
    qoi = dataset.header.metadata["type"]
    unit = dataset.header.unit
    analysis_period = str(dataset.header.analysis_period) # what if tehre are two? 
    spatial_data = get_name_for_spatial_data(dataset)
    return DataDescription(qoi, unit, analysis_period, spatial_data)


# def create_plot_title(dataset: BaseCollection):
#     title = f"{variable} [{unit}] <br><sup> {analysis_period} </sup>"
#     return title


    
def create_init_data(case_name, dataset):
    dd = get_dataset_description(dataset)
    return InitData(case_name, dd.space, dataset.values, dataset.datetimes, dd.qoi)

def extend_data(val, len_data):
    return [val]*len_data

def create_long_dataframe(data:InitData):
    len_data = len(data.values)
    return pl.DataFrame({"case_names": extend_data(data.case_name, len_data),
        "space_names":  extend_data(data.space, len_data),
        "qoi": extend_data(data.qoi, len_data),
        "values": data.values,
        "datetimes": data.datetimes}
    )

def create_dataframe_for_case(case_name, sql, qoi):
    collection = get_collection_for_variable(sql, qoi)
    init_data = [create_init_data(case_name, i) for i in collection]
    dataframes = [create_long_dataframe(i) for i in init_data]
    return pl.concat(dataframes, how="vertical")


def create_dataframe_for_all_cases(cases:list[CaseData], qoi: str):
    dataframes = [create_dataframe_for_case(i.case_name, i.sql, qoi) for i in cases]
    return pl.concat(dataframes, how="vertical")


def create_site_var(case: CaseData, qoi: str):
    try:
        dataset = get_collection_for_variable(case.sql, qoi)[0]
    except ValueError:
        raise Exception("Assuming one analysis peruiod, there should only be one dataset for a site variable!") 
    dd = get_dataset_description(dataset)
    return InitData(case.case_name, dd.space, dataset.values, dataset.datetimes, dd.qoi)

def join_site_data(case: CaseData, qoi: str, df: pl.DataFrame):
    data = create_site_var(case, qoi)
    # types for polars dataframe? 
    cases = df["case_names"].unique()
    len_data = len(data.values)

    # make a copy for each case in the dataframe.. 
    # TODO make sure datetimes are alligned.. 
    def create_case_df(case_name):
        return pl.DataFrame({
            "case_names": extend_data(case_name, len_data),
            "qoi": extend_data(data.qoi, len_data),
            "values": data.values,
            "datetimes": data.datetimes})
    dfs = [create_case_df(i) for i in cases]
    site_df_for_cases = pl.concat(dfs, how="vertical")
    return df.join(site_df_for_cases, on=["case_names", "datetimes"])




def get_plot_labels(case: CaseData, qoi: str):
    collection = get_collection_for_variable(case.sql, qoi)
    dd = get_dataset_description(collection[0])
    case_info = f"Case: {case.case_name}"
    # <br><sup> {dd.analysis_period} </sup> 
    qoi_info = f"{dd.qoi} [{dd.unit}]"
    return case_info, qoi_info


def add_displot_labels(g, case: CaseData, qoi: str):
    case_info, qoi_info = get_plot_labels(case, qoi)
    g.set_xlabels(qoi_info)
    g.figure.suptitle(case_info)
    return g
    


def append_similar_geom_var_to_dataframe(case_name, dataset):
    pass
# qoi1 = 'AFN Linkage Node 1 to Node 2 Volume Flow Rate'
# qoi2 = "Site Wind Speed"
# qoi3 = "Site Wind Direction"
# qoi4 = all_variables.afn.zone["ach"]
# qoi4

# case_data = retrieve_cases()
# sample_case = case_data[0]
# df = create_dataframe_for_all_cases(case_data, qoi4)
# df.head()

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

