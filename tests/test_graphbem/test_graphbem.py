import polars as pl
import pytest
from rich import print as rprint

from plan2eplus.constants import PATH_TO_GRAPHBEM_INPUTS
from plan2eplus.graphbem.cali_study import (
    get_epws_for_graphbem,
    prep_cali_case,
)
from plan2eplus.graphbem.constants import (
    OUTPUT_BASE_PATH,
    SAMPLE_CASE,
    get_output_variables,
    graphbem_additional_variables_fx,
)
from plan2eplus.graphbem.data_helpers import create_dataframe_for_case, DFC
from plan2eplus.graphbem.study import create_graphbem_case
from plan2eplus.helpers.ep_constants import (
    BUILDING_SURFACE,
    OUTPUT_VARIABLE,
    RUNPERIOD,
    SITE,
)
from plan2eplus.helpers.ep_helpers import (
    get_first_object,
    get_zones,
)
from plan2eplus.helpers.helpers import set_intersection
from plan2eplus.helpers.output_requests import request_qoi_variables
from plan2eplus.helpers.variable_interfaces import (
    prepare_to_load_additional_variables_from_file,
)
from plan2eplus.studies.setup.interfaces import CaseData2

EXPECTED_N_ZONES = 4
EXPECTED_OUTPUT_VAR = "Surface Anisotropic Sky Multiplier"
# CALIFORNIA CASES


def test_create_graphbem():
    case = create_graphbem_case()
    idf = case.idf
    zones = get_zones(idf)
    assert len(zones) == EXPECTED_N_ZONES
    # TODO this test is kind of brittle..
    floors = [i for i in idf.idfobjects[BUILDING_SURFACE] if i.Surface_Type == "floor"]
    for floor in floors:
        assert floor.Construction_Name == "My Floor"


def test_can_load_additional_vars():
    path = PATH_TO_GRAPHBEM_INPUTS / "outputs_vars.json"
    assert path.exists()
    get_additional_variables = prepare_to_load_additional_variables_from_file(path)
    assert len(get_additional_variables()) > 1


def test_can_add_additional_vars():
    get_additional_variables = graphbem_additional_variables_fx()
    variable_results = request_qoi_variables(get_additional_variables)

    assert EXPECTED_OUTPUT_VAR in variable_results
    assert len(set(variable_results)) == len(variable_results)


def test_california_case_has_correct_params():
    TEST_EPW = (
        PATH_TO_GRAPHBEM_INPUTS
        / "energyPlus/weather/CAClimateZones/CA_ARCATA-AP_725945S_CZ2022/CA_ARCATA-AP_725945S_CZ2022.epw"
    )
    assert TEST_EPW.exists()

    case = prep_cali_case(TEST_EPW)
    idf = case.idf
    runperiod = get_first_object(idf, RUNPERIOD)
    assert runperiod.Begin_Month == 8
    assert runperiod.End_Month == 8
    assert runperiod.End_Day_of_Month == 31

    site = get_first_object(idf, SITE)
    assert site.Name == "CA_ARCATA-AP"  # this is the

    output_variables = idf.idfobjects[OUTPUT_VARIABLE]
    assert EXPECTED_OUTPUT_VAR in [i.Variable_Name for i in output_variables]


def test_can_get_epw_from_subdirectories():
    epw_files = get_epws_for_graphbem()
    assert len(epw_files) > 0
    for epw in epw_files:
        assert epw.exists()
        assert epw.suffix == ".epw"


# TODO refactor for more general data extraction library..

ZONE_QOI = "Zone Mean Air Temperature"
SITE_QOI = ""
SAMPLE_ZONE_NAME = "corner_ventilation"
SAMPLE_DATE = (2017,8,1)
SAMPLE_HOUR = 0

@pytest.fixture
def case():
    output_path = OUTPUT_BASE_PATH / SAMPLE_CASE
    return CaseData2(output_path)


def test_dataframe_has_correct_rows(case):
    qoi = get_output_variables()[0]
    df = create_dataframe_for_case(case.sql, [qoi], case.idf)

    assert len(df["zone"].unique()) == EXPECTED_N_ZONES # TODO replace names! 
    assert len(df["direction"].unique()) == 6  # num surfaces for rectangular room
    assert len(df["datetimes"].dt.date().unique()) == 31  # number of days in auguest


def test_dataframe_for_multiple_qois_is_correct_surface_only(case):
    qois = get_output_variables()[0:5]
    df =  create_dataframe_for_case(case.sql, qois, case.idf)
    set_vars = set_intersection(list(df.columns), qois)
    print(set_vars)

    assert  set_vars == qois

@pytest.mark.skip("Not yet implemented")
def test_dataframe_for_multiple_qois_is_correct_surface_and_zone(case):
    qois = get_output_variables()[0:3] + [ZONE_QOI]
    df =  create_dataframe_for_case(case.sql, qois, case.idf)
    # zone variable should be the same for all surfaces
    zone_data = df.filter(
            (pl.col("zone") == SAMPLE_ZONE_NAME)
            & (pl.col("datetimes") == pl.date(*SAMPLE_DATE))
        )[ZONE_QOI]
    surfaces = df["direction"].unique()
    assert len(zone_data) == len(surfaces)
    assert len(zone_data.unique()) == 1


# def test_dataframe_for_multiple_qois_is_correct_surface_and_site():
#     df = dataframe_for_one_case_many_qois()


# if __name__ == "__main__":
#     rprint(PATH_TO_GRAPHBEM_INPUTS / "output_vars.json")
#     children = [i for i in PATH_TO_GRAPHBEM_INPUTS.iterdir()]
#     rprint(children)
#     rprint((PATH_TO_GRAPHBEM_INPUTS / "outputs_vars.json").exists())
