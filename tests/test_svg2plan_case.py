import pytest

# from plan2eplus.config import PATH_TO_INPUT_CASES, PATH_TO_OUTPUT_CASES
from plan2eplus.case_edits.ezcase import create_ezcase

inputs_dir = "case_bol_5"
outputs_dir = "test/test25_airwwall"

def test_create_ezcase_from_svg2plan():
    case = create_ezcase(outputs_dir, inputs_dir)
    assert case

def test_ezacase_runs():
    case = create_ezcase(outputs_dir, inputs_dir)
    assert case
    ## run case..
    result = case.run_idf(force_run=True)
    assert result