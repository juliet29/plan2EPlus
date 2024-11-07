from copy import deepcopy
from pathlib import Path

from airflow_network.airboundary import add_air_boundaries, update_air_boundary_constructions
from case_edits.epcase import EneryPlusCaseEditor
from geomeppy import IDF

from helpers.output_requests import add_all_output_requests
from plan.plan_to_eppy import add_eppy_blocks_to_case
from plan.graph_to_subsurfaces import get_subsurface_pairs_from_case
from subsurfaces.creator import add_subsurfaces_to_case
from airflow_network.creator import add_airflownetwork_to_case
from constructions.constructions import CONSTRUCTION_SET_TYPE, assign_cons_set


def get_path_to_inputs(inputs_dir: str):
    path_to_root = Path.cwd().parent / "svg2plan/outputs2/"
    path_to_inputs = path_to_root / inputs_dir
    assert path_to_inputs.exists()
    return path_to_inputs


def get_path_to_outputs(outputs_dir: str):
    path_to_root = Path.cwd() / "cases" 
    path_to_outputs = path_to_root / outputs_dir
    if not path_to_outputs.exists():
        try:
            path_to_outputs.mkdir()
        except:
            path_to_outputs.parent.mkdir()
            path_to_outputs.mkdir()
    return path_to_outputs

def initialize_case(path_to_outputs: Path):
    return EneryPlusCaseEditor(path_to_outputs)



def add_rooms(_idf: IDF, path_to_inputs: Path):
    idf = deepcopy(_idf)
    idf = add_eppy_blocks_to_case(idf, path_to_inputs)
    idf.intersect_match()
    # idf.set_default_constructions()
    return idf


def add_subsurfaces(_idf: IDF, path_to_inputs: Path):
    idf = deepcopy(_idf)
    pairs = get_subsurface_pairs_from_case(path_to_inputs)
    idf = add_subsurfaces_to_case(idf, pairs)
    return idf


def add_airflownetwork(_idf: IDF):
    idf = deepcopy(_idf)
    idf = add_airflownetwork_to_case(idf)
    return idf


def create_ezcase(outputs_dir, inputs_dir, cons_set_type: CONSTRUCTION_SET_TYPE = "Medium"):
    if isinstance(outputs_dir, str) and isinstance(inputs_dir, str):
        path_to_outputs = get_path_to_outputs(outputs_dir)
        path_to_inputs = get_path_to_inputs(inputs_dir)
    else:
        path_to_outputs = outputs_dir
        path_to_inputs = inputs_dir

    case = initialize_case(path_to_outputs) # type: ignore

    case.idf = add_rooms(case.idf, path_to_inputs)
    case.idf = add_subsurfaces(case.idf, path_to_inputs)
    case.idf = assign_cons_set(case.idf, cons_set_type)

    case.idf = add_airflownetwork(case.idf)
    case.idf = add_air_boundaries(case.idf, path_to_inputs)

    case.idf = add_all_output_requests(case.idf)
    case.compare_and_save()
    return case
