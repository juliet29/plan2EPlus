from pprint import pprint
from typing import Optional
from plan2eplus.constants import PATH_TO_GRAPH2PLAN_CASES, PATH_TO_OUTPUT_CASES
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import add_rooms, finish_creating_ezcase
from geomeppy import IDF
from pathlib import Path
from matplotlib import pyplot as plt

from plan2eplus.helpers.geometry_interfaces import Dimensions
from plan2eplus.plan.graph_to_subsurfaces import (
    GraphEdgeJSON,
    create_room_map,
    get_node_mapping,
)
from plan2eplus.helpers.helpers import load_data_from_json
from plan2eplus.subsurfaces.creator import add_subsurfaces_to_case
from plan2eplus.subsurfaces.interfaces import (
    NinePointsLocator,
    SubsurfaceAttributes,
    SubsurfaceObjects,
    SubsurfacePair,
)
from rich import print as rprint
from plan2eplus.visuals.graph_plot import (
    find_points_along_path,
    find_wall_on_zone_facade,
    plot_path_on_plot,
)
from plan2eplus.log_setup import setup_logging
import logging

from plan2eplus.visuals.interfaces import PlanZones
from ladybug.analysisperiod import AnalysisPeriod


logger = logging.getLogger(__name__)
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
    graph_data = load_data_from_json(
        path_to_connectivity_graphs, f"_{graph_ix:02}.json"
    )
    edges: list[GraphEdgeJSON] = graph_data["edges"]
    return [handle_edge(e, room_map) for e in edges]


def create_connectivity_case(
    epw: Optional[Path] = None, analysis_period: Optional[AnalysisPeriod] = None
):
    case = EneryPlusCaseEditor(output_path)
    case.idf = add_rooms(case.idf, input_path)

    n_connectivity_graph = 0
    pairs = get_subsurface_pairs(input_path, n_connectivity_graph)
    case.idf = add_subsurfaces_to_case(case.idf, pairs)
    return case.idf


if __name__ == "__main__":
    setup_logging("test_connectivity")
    logger.info("test_connectivity")
    idf = create_connectivity_case()

    # path = ["NORTH", "c", "a", "SOUTH"]
    path = ["WEST", "b", "a", "EAST"]
    coords = find_points_along_path(idf, path)
    print(f"==>> coords in main: {coords}")
    pz = PlanZones(idf)
    ax = pz.plot_zone_domains()
    _coords = [i.pair for i in coords]
    ax = plot_path_on_plot(_coords, ax)
    plt.show()
