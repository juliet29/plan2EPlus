from pathlib import Path
from ladybug.sql import SQLiteResult
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
    raise Exception(f"Invalid variable request: {var} not in {sql.available_outputs} in {sql}")






