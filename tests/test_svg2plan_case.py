import pytest

# from plan2eplus.config import PATH_TO_INPUT_CASES, PATH_TO_OUTPUT_CASES
from plan2eplus.case_edits.ezcase import create_ezcase

def test_create_ezcase_from_svg2plan():
    inputs_dir = "case_bol_5"
    outputs_dir = "test/test25_airwwall"
    case = create_ezcase(outputs_dir, inputs_dir)
    assert case