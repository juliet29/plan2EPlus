from enum import Enum
from pathlib import Path
from typing import Literal
from ...constants import PATH_TO_OUTPUT_CASES
from ...case_edits.ezcase import get_path_to_inputs 

# from .comparisons import EXP_GROUP
from ...helpers.read_sql import get_sql_results
from ..setup.interfaces import CaseData
from ..setup.setup import get_idf


def retrieve_input_dir(name: str):
    case_name = "_".join(name.split("_")[:2])
    return f"case_{case_name}"


def retrieve_case_from_path(path_to_output: Path):
    idf = get_idf(path_to_output)
    sql = get_sql_results(path_to_output)
    case_name = path_to_output.name
    input_dir = retrieve_input_dir(case_name)
    path_to_input = get_path_to_inputs(input_dir)

    return CaseData(case_name, idf, sql, path_to_input, path_to_output)


def retrieve_cases_from_folder(path_to_dir: Path):
    case_paths = [i for i in path_to_dir.iterdir()]
    return [retrieve_case_from_path(i) for i in case_paths if i.is_dir()]


def get_experiment_folders(exp_group="241119"):
    return [
        i for i in PATH_TO_OUTPUT_CASES.iterdir() if i.is_dir() and exp_group in i.name
    ]


def retrieve_control_cases(exp_group="241119"):
    exp_folders = get_experiment_folders(exp_group)
    [mat_folder] = [i for i in exp_folders if "materials" in i.name]
    return [
        i for i in retrieve_cases_from_folder(mat_folder) if "Medium" in i.case_name
    ]


COMPARISON_GROUPS = Literal["windows", "materials", "doors"]


def retrieve_comparison_groups(comparison_group: COMPARISON_GROUPS, exp_group="241119"):
    exp_folders = get_experiment_folders(exp_group)
    [folder] = [i for i in exp_folders if comparison_group in i.name]
    comparison_cases = [i for i in retrieve_cases_from_folder(folder)]
    if comparison_group == "materials":
        return comparison_cases
    else:
        control_cases = retrieve_control_cases(exp_group)
        return comparison_cases + control_cases



# gt_tbl = (
#     GT(
#         gtcars[["mfr", "model", "hp", "trq", "msrp"]].head(5),
#     )
#     .tab_header(
#         title="Some Cars from the gtcars Dataset",
#         subtitle="Five Cars are shown here"
#     )
#     .tab_spanner(
#         label="Make and Model",
#         columns=["mfr", "model"],
#         id="make_model"
#     )
#     .tab_spanner(
#         label="Performance",
#         columns=["hp", "trq", "msrp"]
#     )
#     .tab_spanner(
#         label="Everything but the cost",
#         columns=["mfr", "model", "hp", "trq"]
#     )
#     .fmt_integer(columns=["hp", "trq"])
#     .fmt_currency(columns="msrp")
#     .tab_source_note("Cars are all 2015 models.")
#     .tab_source_note("Horsepower and Torque values are estimates.")
# )