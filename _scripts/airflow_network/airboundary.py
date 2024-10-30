from pathlib import Path

from geomeppy import IDF
from helpers.helpers import key_from_value
from helpers.ep_helpers import get_partner_of_surface
from plan.helpers import create_room_map, load_data_from_json
from plan.interfaces import GRAPH, GraphEdgeJSON
from subsurfaces.logic import PairOnly, find_surface_connecting_two_zones
from airflow_network.modifiers import create_simple_opening, add_subsurface


def handle_edge_airboundary(
    e: GraphEdgeJSON,
    room_map: dict[int, str],
):
    source, target = e["source"], e["target"]
    return PairOnly(key_from_value(room_map, source), key_from_value(room_map, target))


def get_airboundary_pairs_from_case(path_to_inputs: Path):
    room_map = create_room_map(path_to_inputs)
    graph_data = load_data_from_json(path_to_inputs, GRAPH)
    edges: list[GraphEdgeJSON] = graph_data["links"]
    return [
        handle_edge_airboundary(e, room_map) for e in edges if e["details"]["id"] == 0
    ]

def update_air_boundary_constructions(idf: IDF, path_to_inputs: Path):

    ab_pairs = get_airboundary_pairs_from_case(path_to_inputs)
    for pair in ab_pairs:
        surf = find_surface_connecting_two_zones(idf, pair)
        assert surf

        o = idf.newidfobject("CONSTRUCTION:AIRBOUNDARY")
        o.Name = f"AirBoundary {surf.Name}"
        idf = add_subsurface(idf, surf.Name)
        # idf, opening = create_simple_opening(idf, surf.Name)
        # o.Air_Exchange_Method = opening.Name
        surf.Construction_Name = o.Name 
        partner_surf = get_partner_of_surface(idf, surf)
        assert partner_surf
        partner_surf.Construction_Name = o.Name

    return idf


