from pprint import pprint
from plan2eplus.config import PATH_TO_GRAPH2PLAN_CASES, PATH_TO_OUTPUT_CASES
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import add_rooms, finish_creating_ezcase
from geomeppy import IDF
from pathlib import Path

from plan2eplus.helpers.geometry_interfaces import Dimensions
from plan2eplus.plan.graph_to_subsurfaces import (
    GraphEdgeJSON,
    create_room_map,
    get_node_mapping,
)
from plan2eplus.plan.helpers import load_data_from_json
from plan2eplus.subsurfaces.creator import add_subsurfaces_to_case
from plan2eplus.subsurfaces.interfaces import (
    NinePointsLocator,
    SubsurfaceAttributes,
    SubsurfaceObjects,
    SubsurfacePair,
)
from plan2eplus.studies.analysis.plot_helpers import plot_zone_domains
import matplotlib.pyplot as plt

output_path = PATH_TO_OUTPUT_CASES / "250527_threeplan"
input_path = PATH_TO_GRAPH2PLAN_CASES / "three_plan"

DOOR_DIMENSIONS = (1, 2)


def handle_edge(
    e: GraphEdgeJSON,
    room_map: dict[int, str],
):
    source, target = e["source"], e["target"]
    return SubsurfacePair(
        get_node_mapping(source, room_map),
        get_node_mapping(target, room_map),
        SubsurfaceAttributes(
            object_type=SubsurfaceObjects.DOOR,
            construction=None,
            dimensions=Dimensions(*DOOR_DIMENSIONS),
            location_in_wall=NinePointsLocator.bottom_middle,
        ),
    )


def get_subsurface_pairs(path_to_inputs: Path, graph_ix: int):
    path_to_connectivity_graphs = path_to_inputs / "connectivity"
    room_map = create_room_map(path_to_inputs)
    graph_data = load_data_from_json(path_to_connectivity_graphs, f"_{graph_ix:02}.json")
    edges: list[GraphEdgeJSON] = graph_data["edges"]
    return [
        handle_edge(e, room_map) for e in edges
    ]


def test_connectivity_case():
    case = EneryPlusCaseEditor(output_path)
    case.idf = add_rooms(case.idf, input_path)
    n_connectivity_graph = 0
    pairs = get_subsurface_pairs(input_path, n_connectivity_graph)
    pprint(pairs)
    case.idf = add_subsurfaces_to_case(case.idf, pairs)
    finish_creating_ezcase(case, input_path)


    fig, ax = plt.subplots()
    plot_zone_domains(case.idf, ax)
    plt.show()

    case.idf.printidf()
    case.run_idf(force_run=True)


    return fig


if __name__ == "__main__":
    print("Running connectivity test..")
    test_connectivity_case()
