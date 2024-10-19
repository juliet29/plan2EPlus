from copy import deepcopy
from pathlib import Path

from case_edits.interfaces import EzCaseInput
from case_edits.epcase import EneryPlusCaseEditor
from geomeppy import IDF

from new_subsurfaces.interfaces import SubsurfacePair
from plan.convert import add_eppy_blocks_to_case
from plan.interfaces import PlanAccess
from plan.subsurface_translator import SubsurfaceTranslator
from methods.airflownetwork import AirflowNetwork


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

def add_rooms_to_case(_idf:IDF, access: PlanAccess):
    idf = deepcopy(_idf)
    idf = add_eppy_blocks_to_case(idf, access)
    idf.intersect_match()
    idf.set_default_constructions()
    return idf


def add_subsurfaces(case_path: Path):
    st = SubsurfaceTranslator(case_path)
    st.run()
    # TODO actually create subsurfaces. 
    return st.pairs

    pass
    # if self.inputs.subsurface_pairs:
    #     self.get_subsurface_constructions()
    #     inputs = SubsurfaceCreatorInputs(
    #         self.zones, self.inputs.subsurface_pairs, self.case.idf
    #     )
    #     self.ss = SubsurfaceCreator(inputs)
    #     self.ss.create_all_ssurface()
    #     self.case.geometry.update_geometry_subsurfaces()

def add_airflownetwork(case):
        return AirflowNetwork(case)


def create_ezcase(outputs_dir, inputs_dir):
    path_to_inputs = get_case_inputs_path(inputs_dir)
    case = initialize_case(outputs_dir)
    case.idf = add_rooms_to_case(case.idf, PlanAccess(path_to_inputs, 0))
    return case.idf