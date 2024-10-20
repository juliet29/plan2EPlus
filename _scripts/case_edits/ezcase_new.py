from copy import deepcopy
from pathlib import Path

from case_edits.interfaces import EzCaseInput
from case_edits.epcase import EneryPlusCaseEditor
from geomeppy import IDF

from new_subsurfaces.creator import add_subsurfaces_to_case
from new_subsurfaces.interfaces import SubsurfacePair
from plan.convert import add_eppy_blocks_to_case
from plan.interfaces import PlanAccess
from plan.subsurface_translator import get_subsurface_pairs_from_case
# from methods.airflownetwork import AirflowNetwork


def get_case_inputs_path(inputs_dir: str):
    path_to_root = Path.cwd().parent / "svg2plan/outputs2/"
    path_to_case = path_to_root / inputs_dir
    assert path_to_case.exists()
    return path_to_case

def initialize_case(case_name:str):
    return EneryPlusCaseEditor(
        case_name, "", ""
        # inputs.starting_case,
        # project_name=inputs.project_name,
    )

def add_rooms(_idf:IDF, case_path: Path):
    idf = deepcopy(_idf)
    idf = add_eppy_blocks_to_case(idf, PlanAccess(case_path, 0))
    idf.intersect_match()
    idf.set_default_constructions()
    return idf


def add_subsurfaces(_idf:IDF, case_path: Path):
    idf = deepcopy(_idf)
    pairs = get_subsurface_pairs_from_case(case_path)
    idf = add_subsurfaces_to_case(idf, pairs)
    return idf
    


# def add_airflownetwork(case):
#         return AirflowNetwork(case)


def create_ezcase(outputs_dir, inputs_dir):
    path_to_inputs = get_case_inputs_path(inputs_dir)
    case = initialize_case(outputs_dir)
    case.idf = add_rooms(case.idf, path_to_inputs)
    case.idf = add_subsurfaces(case.idf, path_to_inputs)
    return case.idf