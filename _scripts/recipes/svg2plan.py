from copy import deepcopy
from pathlib import Path

# from case_edits.ezcase import EzCaseInput
from case_edits.ezcase import EzCase
from case_edits.ezcase_new import EzCaseInput
from new_subsurfaces.interfaces import SubsurfacePair as SSP
# from methods.subsurfaces.pairs import SubsurfaceObjects
# from methods.subsurfaces.pairs import DEFAULT_WINDOW
# from geometry.wall_normal import WallNormal
from plan.subsurface_translator import SubsurfaceTranslator
# from case_edits.ezcase import EzCaseInput
# from recipes.two_zone import output_reqs
# from plan.interfaces import RoomAccess

CASE = "tests/test22_svg2plan"
PLAN_DIR = "amber_a"
PLAN_INDEX = 0


def get_case_inputs_path(case_name: str):
    path_to_root = Path.cwd().parent / "svg2plan/outputs2/"
    path_to_case = path_to_root / case_name
    assert path_to_case.exists()

    return path_to_case

# def create_inputs(case_name: str):
#     case_path = initialize_case(case_name)
#     EzCaseInput(case_name=CASE, )
#     # st = SubsurfaceTranslator(case_path)
#     # st.run()




    # input = EzCaseInput(
    #     case_name=CASE,
    #     geometry=GPLANRoomAccess(st.gplan_path, PLAN_INDEX),
    #     # subsurface_pairs=[],
    #     subsurface_pairs=st.pairs,
    #     output_variables=output_reqs,)