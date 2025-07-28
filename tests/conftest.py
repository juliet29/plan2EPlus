import pytest

from plan2eplus.case_edits.epcase import read_existing_idf 
from plan2eplus.paths import path_class


TEST_CASE = "three_plan"
EXPECTED_N_ZONES = 3


@pytest.fixture()
def defaults():
    return TEST_CASE, EXPECTED_N_ZONES

@pytest.fixture()
def test_case():
    return read_existing_idf(path_class.models / TEST_CASE) 
