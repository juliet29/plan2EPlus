from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple
from ladybug.sql import SQLiteResult
from ladybug.dt import DateTime
from geomeppy import IDF

from plan2eplus.constants import DEFAULT_IDF_NAME
from plan2eplus.graphbem.study import EneryPlusCaseEditor
from plan2eplus.helpers.read_sql import (
    DEFAULT_SQL_SUBPATH,
    get_sql_results,
)
from plan2eplus.case_edits.epcase import read_existing_idf


class CaseData(NamedTuple):
    case_name: str
    idf: IDF
    sql: SQLiteResult
    path_to_input: Path


@dataclass
class CaseData2:
    path_to_output: Path

    def __post_init__(self):
        assert self.path_to_output.exists(), "Invalid path"

    @property
    def idf(self) -> IDF:
        case = read_existing_idf(self.path_to_output)
        return case.idf


    @property
    def sql(self) -> SQLiteResult:
        return get_sql_results(self.path_to_output)

    @property
    def case_name(self) -> str:
        return self.path_to_output.stem


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
