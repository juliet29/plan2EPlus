from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Literal, NamedTuple
from ladybug.sql import SQLiteResult
from ladybug.datacollection import BaseCollection
from warnings import warn
from plan2eplus.constants import DEFAULT_SQL_SUBPATH
from plan2eplus.helpers.helpers import check_list_has_identical_items
from rich import print as rprint 


SpaceTuple = NamedTuple("SpaceTuple", [("name", str), ("space_type", str)])


class SpaceTypes(StrEnum):
    SYSTEM = "System"
    ZONE = "Zone"
    SURFACE = "Surface"


# SpaceTypes = Literal["System", "Zone", "Surface"]


def get_name_for_spatial_data(dataset: BaseCollection):
    keys = dataset.header.metadata.keys()
    space_types = [i.value for i in SpaceTypes]
    # print(keys)
    for i in space_types:
        if i in keys:
            return SpaceTuple(dataset.header.metadata[i], i)
    else:
        raise Exception(f"Spatial type is not defined: {keys}")


@dataclass
class SQLCollection:
    collection: BaseCollection

    @property
    def values(self):
        return self.collection.values

    @property
    def datetimes(self):
        return self.collection.datetimes

    @property
    def qoi(self):
        return self.collection.header.metadata["type"]

    @property
    def unit(self):
        return self.collection.header.unit

    @property
    def analysis_period(self):
        return self.collection.header.analysis_period

    @property
    def space_tuple(self):
        return get_name_for_spatial_data(self.collection)

    @property
    def space_name(self):
        return self.space_tuple.name

    @property
    def space_type(self):
        return self.space_tuple.space_type


def get_sql_results(path_to_outputs: Path):
    SQL_PATH = path_to_outputs / DEFAULT_SQL_SUBPATH
    assert SQL_PATH.exists(), "Invalid folder organization"
    return SQLiteResult(str(SQL_PATH))


def validate_request(sql: SQLiteResult, var: str):
    assert sql.available_outputs is not None
    try:
        assert var in sql.available_outputs
        return True
    except AssertionError:
        warn(f"{var} not in available_outputs")
        return False


def create_collections_for_variable(sql: SQLiteResult, var: str) -> list[SQLCollection]:
    """Returns a collection for each space"""
    if validate_request(sql, var):
        collections: list[BaseCollection] = sql.data_collections_by_output_name(var)
        assert len(collections) > 0, "No collections found!"

        datasets = [SQLCollection(i) for i in collections]

        try:
            check_list_has_identical_items([i.space_type for i in datasets])
        except AssertionError:
            raise NotImplementedError(f"[red bold] This collection for {var} has multiple space types!")


        return datasets

    raise Exception(
        f"Invalid variable request: {var} not in {sql.available_outputs} in {sql}"
    )
