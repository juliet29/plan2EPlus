from pathlib import Path
from munch import Munch
from ladybug.sql import SQLiteResult
import plotly.graph_objects as go
from ladybug.datacollection import BaseCollection
from warnings import warn


def get_sql_results(path_to_outputs: Path):
    SQL_PATH = path_to_outputs / "results" / "eplusout.sql"
    assert SQL_PATH.exists()
    return SQLiteResult(str(SQL_PATH))


def validate_request(sql: SQLiteResult, var: str):
    assert sql.available_outputs is not None
    try:
        assert var in sql.available_outputs
        return True
    except AssertionError:
        warn(f"{var} not in available_outputs")
        return False


def get_collection_for_variable(sql: SQLiteResult, var: str) -> BaseCollection:
    if validate_request(sql, var):
        collection = sql.data_collections_by_output_name(var)
        return collection
        # split_collection_by_ap(collection)
    raise Exception(f"Invalid variable request")


# TODO move


def create_plot_title(dataset: BaseCollection):
    variable = dataset.header.metadata["type"]
    unit = dataset.header.unit
    analysis_period = str(dataset.header.analysis_period)
    title = f"{variable} [{unit}] <br><sup> {analysis_period} </sup>"
    return title


def line_plots(collections: list[BaseCollection]):
    fig = go.Figure()

    def get_name_for_system(dataset):
        try:
            return dataset.header.metadata["System"]
        except:
            try:
                return dataset.header.metadata["Zone"]
            except:
                return dataset.header.metadata["Surface"]


    for dataset in collections:
        name = get_name_for_system(dataset)
        fig.add_trace(go.Scatter(x=dataset.datetimes, y=dataset.values, name=name))

    title = create_plot_title(dataset)
    fig.update_layout(title_text=title)

    return fig


# def split_collection_by_ap(collection):
#     collection_by_ap = Munch()
#     for dataset in collection:
#         # TODO maybe use a shorter name..
#         ap = str(dataset.header.analysis_period)
#         if ap not in collection_by_ap.keys():
#             collection_by_ap.update({ap: []})
#         collection_by_ap[ap].append(dataset)

# def filter_collections():
#     if analysis_period == None:
#         set_analysis_period()
#     filtered_collection = collection_by_ap[analysis_period]
#     get_collection_geometry_type(filtered_collection[0])


# def set_analysis_period(ix=0):
#     # TODO issue => what if dont have a collection yet.. actually no bc will have called the stuff above..
#     possible_ap = list(collection_by_ap.keys())
#     assert possible_ap, "No analysis periods"
#     analysis_period = possible_ap[ix]


# def show_analysis_periods():
#     for ix, k in enumerate(collection_by_ap.keys()):
#         print(f"{ix} - {k}")

# def get_var_data(var:OutputVars):
#     get_collection_for_variable(var)
#     filter_collections()
#     return filtered_collection

# def get_collection_geometry_type(dataset):
#     metadata = dataset.header.metadata
#     types = ["System", "Zone", "Surface"]

#     for curr_type in types:
#         try:
#             metadata[curr_type]
#             geom_type = curr_type
#             return
#         except:
#             pass
#     raise Exception(f"didnt find type {curr_type}")
