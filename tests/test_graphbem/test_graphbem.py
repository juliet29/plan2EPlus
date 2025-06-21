from plan2eplus.constants import PATH_TO_GRAPHBEM_INPUTS
from rich import print as rprint
from plan2eplus.helpers.output_requests import request_qoi_variables
from plan2eplus.helpers.variable_interfaces import prepare_to_load_additional_variables_from_file


# def test_weather_path_is_correct():
#     assert PATH_TO_GRAPHBEM_INPUTS.exists()


# def test_analysis_period_is_updated():
#     pass


def test_can_load_additional_vars():
    path = PATH_TO_GRAPHBEM_INPUTS / "outputs_vars.json"
    rprint(path.exists())
    get_additional_variables = prepare_to_load_additional_variables_from_file(path)
    assert len(get_additional_variables()) > 1


def test_can_add_additional_vars():
    path = PATH_TO_GRAPHBEM_INPUTS / "outputs_vars.json"
    get_additional_variables = prepare_to_load_additional_variables_from_file(path)
    
    expected_var = "Surface Anisotropic Sky Multiplier"
    variable_results = request_qoi_variables(get_additional_variables)

    assert expected_var in variable_results
    assert len(set(variable_results)) == len(variable_results)


if __name__ == "__main__":
    rprint(PATH_TO_GRAPHBEM_INPUTS / "output_vars.json")
    children = [i for i in PATH_TO_GRAPHBEM_INPUTS.iterdir()]
    rprint(children)
    rprint((PATH_TO_GRAPHBEM_INPUTS / "outputs_vars.json").exists())