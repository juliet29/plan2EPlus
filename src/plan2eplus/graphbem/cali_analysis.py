from pathlib import Path
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


def write_csv_for_one_case(output_path: Path, variables: list[str] ):
    case = CaseData2(output_path)
    df =  create_dataframe_for_case(case.sql, variables, case.idf)
    assert len(df.columns) > len(variables)
    file_name = "surface_data.csv"
    path = output_path /file_name
    rprint(f"path to print to is {path}")
    assert path.parent.exists(), f"{path} does not exist!"
    df.write_csv(file = path)
    return df 

def write_csvs_for_all_cases_and_all_surface_qois():
    variables =  get_output_variables()
    case_paths = [i for i in OUTPUT_BASE_PATH.iterdir() if i.is_dir()]
    for case in case_paths:
        rprint(f"Preparing case for {case.stem}")

        write_csv_for_one_case(case, variables)
        # except:
        #     rprint(f"[red bold] Printing {case} failed")
        #     pass
    




if __name__ == "__main__":
    print("Analyzing california studies.. ")
    write_csvs_for_all_cases_and_all_surface_qois()
 