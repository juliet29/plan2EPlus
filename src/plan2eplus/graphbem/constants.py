from plan2eplus.constants import PATH_TO_GRAPHBEM_INPUTS, PATH_TO_OUTPUT_CASES
from plan2eplus.helpers.variable_interfaces import (
    prepare_to_load_additional_variables_from_file,
)


WEATHER_PATH = PATH_TO_GRAPHBEM_INPUTS / "energyPlus/weather/CAClimateZones/"
OUTPUT_BASE_PATH = PATH_TO_OUTPUT_CASES / "graphbem_cali"
SAMPLE_CASE = "CA_ARCATA-AP_725945S_CZ2022"


def graphbem_additional_variables_fx():
    path = PATH_TO_GRAPHBEM_INPUTS / "outputs_vars.json"
    get_additional_variables = prepare_to_load_additional_variables_from_file(path)

    return get_additional_variables


# get variables.


def get_output_variables():
    get_vars = graphbem_additional_variables_fx()
    return get_vars()
