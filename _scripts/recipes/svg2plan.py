from copy import deepcopy
from pathlib import Path

from case_edits.ezcase import EzCaseInput
from methods.subsurfaces.pairs import SubsurfacePair as SSP
from methods.subsurfaces.pairs import SubsurfaceObjects
from methods.subsurfaces.pairs import DEFAULT_WINDOW
from geometry.wall_normal import WallNormal


from plan.room_class import GPLANRoomAccess
from plan.subsurface_translator import SubsurfaceTranslator
from case_edits.ezcase import EzCaseInput
from recipes.two_zone import output_reqs

CASE = "tests/test22_svg2plan"
PLAN_DIR = "amber_a"
PLAN_INDEX = 0


def initialize_case(case_name: str):
    path_to_root = Path.cwd().parent / "svg2plan/outputs2/"
    path_to_case = path_to_root / case_name
    assert path_to_case.exists()

    # st = SubsurfaceTranslator(path_to_case)
    # st.run()

    return path_to_case


    # input = EzCaseInput(
    #     case_name=CASE,
    #     geometry=GPLANRoomAccess(st.gplan_path, PLAN_INDEX),
    #     # subsurface_pairs=[],
    #     subsurface_pairs=st.pairs,
    #     output_variables=output_reqs,)