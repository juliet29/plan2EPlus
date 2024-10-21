from pathlib import Path
from munch import Munch
from ladybug.sql import SQLiteResult
from warnings import warn




def get_sql_results(path_to_outputs:Path):
    SQL_PATH = path_to_outputs / "results" / "eplusout.sql"
    assert SQL_PATH.exists()
    return SQLiteResult(str(SQL_PATH))
    
def validate_request(sql: SQLiteResult, var:str):
    assert sql.available_outputs is not None
    try:
        assert var in sql.available_outputs
        return True
    except AssertionError:
        warn(f"{var} not in available_outputs")  
        return False

def get_collection_for_variable(sql: SQLiteResult, var:str):
    if validate_request(sql, var):
        collection = sql.data_collections_by_output_name(
            var
        )
        return collection
        # split_collection_by_ap(collection)


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