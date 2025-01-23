from pathlib import Path
from geomeppy import IDF
from eppy.runner.run_functions import EnergyPlusRunError
from ...case_edits.ezcase import create_ezcase, get_path_to_inputs, get_path_to_outputs

from ...helpers.read_sql import get_sql_results
from .interfaces import CaseData

DEFAULT_OUTPUTS_FOLDER = "oct_h4h_plans"
AIRBOUNDARY_FOLDER = "airboundary"


def get_case_names():
    return ["amb_b1", "bol_5", "red_b1"]


def create_directories(outputs_folder=DEFAULT_OUTPUTS_FOLDER):
    case_names = get_case_names()
    input_dirs = [f"case_{i}" for i in case_names]

    output_dirs = [f"{outputs_folder}/{i}" for i in input_dirs]

    return list(zip(input_dirs, output_dirs, case_names))


def retrieve_paths(input_dir, output_dir):
    path_to_input = get_path_to_inputs(input_dir)
    path_to_output = get_path_to_outputs(output_dir)
    return path_to_input, path_to_output


def create_cases(outputs_folder=DEFAULT_OUTPUTS_FOLDER):
    def create_case(dirs):
        input_dir, output_dir, _ = dirs
        case = create_ezcase(output_dir, input_dir)
        try:
            case.run_idf(force_run=False)
        except EnergyPlusRunError:
            raise Exception

    for i in create_directories(outputs_folder):
        create_case(i)
    return True


def get_idf(path_to_output: Path):
    idf_path = path_to_output / "out.idf"
    return IDF(idf_path)


def retrieve_case_data(input_dir, output_dir, case_name):
    path_to_input, path_to_output = retrieve_paths(input_dir, output_dir)
    idf = get_idf(path_to_output)
    sql = get_sql_results(path_to_output)
    return CaseData(case_name, idf, sql, path_to_input, path_to_output)


def retrieve_cases(outputs_folder=DEFAULT_OUTPUTS_FOLDER):
    return [retrieve_case_data(*i) for i in create_directories(outputs_folder)]


def retrieve_test_case(output_dir, case_name="test"):
    path_to_input = get_path_to_inputs(f"case_bol_5")
    path_to_output = get_path_to_outputs(f"tests/{output_dir}")
    idf = get_idf(path_to_output)
    sql = get_sql_results(path_to_output)
    return CaseData(case_name, idf, sql, path_to_input, path_to_output)


# def get_sqls(case_data: list[CaseData]):
#     return sqls
