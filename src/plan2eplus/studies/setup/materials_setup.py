from itertools import product
from .setup import get_case_names, retrieve_case_data
from eppy.runner.run_functions import EnergyPlusRunError
from ...case_edits.ezcase import create_ezcase

MAT_OUTPUTS_FOLDER = "material_exp"


def create_directories():
    case_names = get_case_names()
    input_dirs = [f"case_{i}" for i in case_names]

    outputs_folder = MAT_OUTPUTS_FOLDER
    construction_types = ["Light", "Medium", "Heavy"]

    output_combos = list(product(construction_types, input_dirs))
    mat_case_names = [f"{c}_{i}" for c, i in output_combos]

    output_dirs = [f"{outputs_folder}/{m}" for m in mat_case_names]

    return list(zip(input_dirs * 3, output_dirs, mat_case_names))


def create_materials_cases():
    def create_case(dirs):
        input_dir, output_dir, case_name = dirs
        mat = case_name.split("_")[0]
        print(input_dir, output_dir, case_name)
        case = create_ezcase(output_dir, input_dir, mat)
        try:
            case.run_idf(force_run=True)
        except EnergyPlusRunError:
            raise Exception

    for i in create_directories():
        create_case(i)
    return True


def retrieve_cases():
    return [retrieve_case_data(*i) for i in create_directories()]
