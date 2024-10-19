from operator import attrgetter
from typing import List, Tuple, Union, Sequence, NamedTuple
from munch import Munch

from new_subsurfaces.interfaces import SubsurfacePair
from outputs.variables import OutputVars as OV
from plan.interfaces import PlanAccess
 

class EzCaseInput:
    case_name: str
    subsurface_pairs: Union[List[SubsurfacePair], List]
    output_variables: List[OV]
    access: PlanAccess
    starting_case: str = ""
    project_name: str = ""