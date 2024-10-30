from pathlib import Path
from eppy.bunch_subclass import EpBunch
from geomeppy import IDF
from helpers.helpers import key_from_value
from helpers.ep_helpers import get_partner_of_surface, get_surface_by_name
from plan.helpers import create_room_map, load_data_from_json
from plan.interfaces import GRAPH, GraphEdgeJSON
from subsurfaces.logic import PairOnly, find_surface_connecting_two_zones
from airflow_network.modifiers import add_zone, create_simple_opening, add_subsurface

def get_airboundary_wall(airboundary: EpBunch):
    n = airboundary.Name
    remain = n.split(" ")[1:]
    return " ".join(remain)

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
        surf.Construction_Name = o.Name 
        partner_surf = get_partner_of_surface(idf, surf)
        assert partner_surf
        partner_surf.Construction_Name = o.Name

    return idf

def get_afn_zone(idf: IDF):
    afn_zones = idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]
    assert afn_zones, "Subsurface AFN zones have not been added"
    return [i.Zone_Name for i in afn_zones]


def update_afn_for_airboundary_zones(idf: IDF):

    
    airboundaries =idf.idfobjects["CONSTRUCTION:AIRBOUNDARY"]
    for ab in airboundaries:
        wall = get_surface_by_name(idf, get_airboundary_wall(ab))
        assert wall
        partner_wall = get_partner_of_surface(idf, wall)
        assert partner_wall
        # print(wall.Name, "/", wall.Zone_Name, "/", partner_wall.Name, "/", partner_wall.Zone_Name)
        afn_zone_names = get_afn_zone(idf)

        if wall.Zone_Name not in afn_zone_names:
            print(f"{wall.Zone_Name} not in  original AFN. Adding now.. " ) 
            idf = add_zone(idf, wall.Zone_Name)

        afn_zone_names = get_afn_zone(idf)
        if partner_wall.Zone_Name not in afn_zone_names:
            print(f"{partner_wall.Zone_Name} not in  original AFN. Adding now.. " ) 
            idf = add_zone(idf, partner_wall.Zone_Name)

    return idf

def add_air_boundaries(idf: IDF, path_to_inputs: Path):
    idf = update_air_boundary_constructions(idf, path_to_inputs)
    idf = update_afn_for_airboundary_zones(idf)

    return idf
            


