from ...epcase import EneryPlusCaseEditor
from ...case_edits.ezcase import get_path_to_inputs, get_path_to_outputs
from experiments.comparisons import get_input_dir
from ...helpers.ep_geom_helpers import get_zone_domains
from .helpers import get_domains_lim
from ...helpers.geometry_interfaces import Range, Domain
from plan.plan_to_eppy import add_eppy_blocks_to_case
from ..setup.setup import get_case_names


output_path = get_path_to_outputs("test/plan_details")


def get_input_paths():
    input_dirs = [get_input_dir(i) for i in get_case_names()]
    return [get_path_to_inputs(i) for i in input_dirs]


def init_case(input_path):
    case = EneryPlusCaseEditor(output_path)
    case.idf = add_eppy_blocks_to_case(case.idf, input_path)
    return get_zone_domains(case.idf)


def get_plan_area(zone_domains: list[Domain]):
    return sum([z.area for z in zone_domains])


def get_plan_aspect_ratio(zone_domains: list[Domain]):
    x_diff, y_diff = get_domains_lim(zone_domains, 0)
    plan_domain = Domain(Range(*x_diff), Range(*y_diff))
    return plan_domain.aspect_ratio
