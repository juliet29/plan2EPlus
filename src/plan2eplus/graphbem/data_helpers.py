from typing import Optional

from geomeppy import IDF
from plan2eplus.helpers.helpers import extend_data
from plan2eplus.helpers.read_sql import (
    SQLCollection,
    SQLiteResult,
    create_collections_for_variable,
    SpaceTypes,
)
from plan2eplus.visuals.interfaces import Surface, Zone
import polars as pl

from copy import deepcopy
from enum import StrEnum


class DFC(StrEnum):
    """Dataframe Columns"""

    ZONE = "zone"
    DIRECTION = "direction"
    IS_EXTERIOR = "is_exterior"
    CASE_NAMES = "case_names"
    SPACE_NAMES = "space_names"
    DATETIMES = "datetimes"


def add_space_name_details(
    geom: Zone | Surface, _data_dict: dict[str, list], len_data: int
):
    data_dict = deepcopy(_data_dict)
    data_dict[DFC.ZONE.value] = extend_data(geom.dname.plan_name_alone, len_data)

    if not isinstance(geom, Zone):
        surf = geom
        data_dict[DFC.DIRECTION.value] = extend_data(surf.direction.name, len_data)
        data_dict[DFC.IS_EXTERIOR.value] = extend_data(not surf.is_interior, len_data)

    return data_dict


def handle_add_space_name_details(
    collection: SQLCollection, idf: IDF, data_dict: dict[str, list]
):
    # TODO write tests for different speace types!
    match collection.space_type:
        case SpaceTypes.ZONE.value | SpaceTypes.SYSTEM.value:
            geom = Zone.create(idf, collection.space_name)
        case SpaceTypes.SURFACE.value:
            geom = Surface.create(idf, collection.space_name)
        case _:
            raise NotImplementedError(
                f"Havent handled this type of surface..{collection.space_type} "
            )
    len_data = len(collection.values)
    return add_space_name_details(geom, data_dict, len_data)


def create_long_dataframe(
    collection: SQLCollection,
    idf: Optional[IDF] = None,
    case_name: Optional[str] = None,
):
    len_data = len(collection.values)
    data_dict: dict[str, list] = {}

    if case_name:
        data_dict[DFC.CASE_NAMES.value] = extend_data(case_name, len_data)

    data_dict[DFC.SPACE_NAMES.value] = extend_data(collection.space_name, len_data)
    if idf:
        data_dict = handle_add_space_name_details(collection, idf, data_dict)

    data_dict[DFC.DATETIMES.value] = list(collection.datetimes)

    return pl.DataFrame(data_dict).with_columns(
        pl.Series(name=collection.qoi, values=collection.values)
    )


def dataframe_for_qoi(
    sql: SQLiteResult,
    qoi: str,
    idf: Optional[IDF] = None,
    case_name: Optional[str] = None,
):
    collections = create_collections_for_variable(sql, qoi)
    dataframes = [create_long_dataframe(collection, idf, case_name) for collection in collections]
    df1 = pl.concat(dataframes, how="vertical")
    return df1


def create_dataframe_for_case(
    sql: SQLiteResult,
    qois: list[str],
    idf: Optional[IDF] = None,
    case_name: Optional[str] = None,
):
    df0 = dataframe_for_qoi(sql, qois[0], idf, case_name)
    if len(qois) == 1:
        return df0
    remaining_dfs = [dataframe_for_qoi(sql, qoi) for qoi in qois[1:]]
    # collections = create_collections_for_variable(sql, qois[0])
    # dataframes = [
    #     create_long_dataframe(collection, idf, case_name) for collection in collections
    # ]
    # df0 = pl.concat(dataframes, how="vertical")
   
    # if have many qois.. assume that have matching surface type..
    # df1 = dataframe_for_qoi(sql, qois[1])
    # df2 = dataframe_for_qoi(sql, qois[2])
    # df0.join(df1, on = [DFC.SPACE_NAMES.value, DFC.DATETIMES.value])
    return pl.concat([df0] + remaining_dfs, how="align")
