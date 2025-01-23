from pathlib import Path
from geomeppy import IDF
import polars as pl
from ...helpers.ep_helpers import get_zone_num
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from ..network.network import create_base_graph, get_node_partners
from ...plan.helpers import create_room_map
from ..setup.data_wrangle import create_dataframe_for_case
from ..setup.interfaces import CaseData


def get_min_max(medians: pl.DataFrame, col=None):
    if not col:
        numeric_values = medians.select(pl.selectors.numeric())
        min_val = numeric_values.min_horizontal().min()
        max_val = numeric_values.max_horizontal().max()

    else:
        series = medians[col]
        return series.min(), series.max()

    return min_val, max_val


def true_min_max(min_max_pairs: list[tuple[float, float]]):
    min_val = min([m[0] for m in min_max_pairs])
    max_val = max([m[1] for m in min_max_pairs])
    return min_val, max_val


def convert_zone_space_name(room_map: dict[int, str], name):
    try:
        ix = get_zone_num(name)
        room_name = room_map[ix]
        return f"{ix}-{room_name}"
    except:
        return name


def normalize_column(df: pl.DataFrame, col: str, range=(1, 3)):
    vals = np.absolute(df[col].to_numpy().reshape(-1, 1))
    scaler = MinMaxScaler(feature_range=range)
    scaler.fit(vals)
    return scaler.transform(vals).reshape(1, -1)[0]


def link_dfs_for_qois(case: CaseData, qois: list[str]):
    df = [create_dataframe_for_case(case.case_name, case.sql, qoi) for qoi in qois]
    return pl.concat(df, how="vertical")


def map_zone_names(path_to_input: Path, df: pl.DataFrame):
    room_map = create_room_map(path_to_input)
    fx = lambda name: convert_zone_space_name(room_map, name)
    return df.with_columns(
        room_names=pl.col("space_names").map_elements(fx, return_dtype=pl.String),
    )


def map_linkage_names_to_G(idf: IDF, path_to_input: Path, df: pl.DataFrame):
    G, _ = create_base_graph(idf, path_to_input)
    fx = lambda surf_name: get_node_partners(idf, G, surf_name)
    return df.with_columns(
        room_pairs=pl.col("space_names").map_elements(fx, return_dtype=pl.Object)
    )


def extract_times(df: pl.DataFrame):
    return df.with_columns(time=pl.col("datetimes").dt.to_string("%H:%M"))
