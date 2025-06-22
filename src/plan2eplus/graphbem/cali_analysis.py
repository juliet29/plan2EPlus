import polars as pl
from plan2eplus.graphbem.constants import (
    OUTPUT_BASE_PATH,
    SAMPLE_CASE,
    get_output_variables,
)
from plan2eplus.graphbem.data_helpers import create_dataframe_for_case
from plan2eplus.helpers.read_sql import get_sql_results
from rich import print as rprint

from plan2eplus.studies.setup.interfaces import CaseData2
import polars as pl


def dataframe_for_one_case():
    output_path = OUTPUT_BASE_PATH / SAMPLE_CASE
    case = CaseData2(output_path)
    test_var = get_output_variables()[0:4]
    return create_dataframe_for_case(case.sql, test_var, case.idf)


if __name__ == "__main__":
    SAMPLE_ZONE_NAME = "corner_ventilation"
    SAMPLE_DATE = (2017,8,1)
    SAMPLE_HOUR = 0
    print("Analyzing california studies.. ")
    df = dataframe_for_one_case()
    # f = df.filter(
    #     (pl.col("zone") == SAMPLE_ZONE_NAME)
    #     & (pl.col("datetimes") == pl.datetime(*SAMPLE_DATE))
    #     # & (pl.col("hour") == SAMPLE_HOUR)
    # )

    rprint(df)