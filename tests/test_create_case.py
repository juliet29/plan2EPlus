from os import fpathconf

import pytest
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import add_rooms, finish_creating_ezcase
from plan2eplus.helpers.ep_helpers import get_zones
from plan2eplus.paths import path_class
from rich import print as rprint

from plan2eplus.visuals.interfaces import PlanZones 



def test_create_case(tmp_path, defaults):
    TEST_CASE, EXPECTED_N_ZONES = defaults
    case = EneryPlusCaseEditor(path_to_outputs=tmp_path)
    case.idf = add_rooms(case.idf, path_to_inputs=path_class.plans / TEST_CASE)
    zones = get_zones(case.idf)
    assert len(zones) == EXPECTED_N_ZONES


# TODO -> test adding subsurfaces
# TODO -> test adding materials
# TODO -> test running case, save in temp dir.. 

@pytest.mark.skip("slow")
def test_running_case_simple(tmp_path, defaults):
    TEST_CASE, _ = defaults
    case = EneryPlusCaseEditor(path_to_outputs=tmp_path)
    case.idf = add_rooms(case.idf, path_to_inputs=path_class.plans / TEST_CASE)
    case = finish_creating_ezcase(case)
    assert case.run_idf(force_run=True)





if __name__ == "__main__":
    pass
    # case = test_create_three_plan_case()
    # test_running_case_simple()
    # case.run_idf(force_run=True)