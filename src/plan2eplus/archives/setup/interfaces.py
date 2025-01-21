from pathlib import Path
from typing import NamedTuple
from ladybug.sql import SQLiteResult
from ladybug.dt import DateTime
from geomeppy import IDF


class CaseData(NamedTuple):
    case_name: str
    idf: IDF
    sql: SQLiteResult
    path_to_input: Path
    path_to_output: Path


class DataDescription(NamedTuple):
    qoi: str
    unit: str
    analysis_period: str
    space: str


class InitData(NamedTuple):
    case_name: str
    space: str
    values: list[float]
    datetimes: list[DateTime]
    qoi: str
