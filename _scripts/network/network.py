# plot nodes and labels..
from pathlib import Path
from typing import Optional
from geomeppy import IDF

import networkx as nx
from network.cardinal_positions import create_cardinal_positions, NodePositions
from plan.graph_to_subsurfaces import get_subsurface_pairs_from_case
from plan.helpers import create_room_map
from helpers.ep_helpers import get_surface_direction, get_zones, WallNormal
from helpers.ep_geom_helpers import create_domain_for_zone
from subsurfaces.interfaces import SubsurfacePair
from subsurfaces.logic import get_connecting_surface
from typing import NamedTuple, TypedDict, Literal


class EdgeDetails(TypedDict):
    surface: str
    subsurfaces: str
    stype: Literal["WINDOW", "DOOR"]


class GraphEdge(NamedTuple):
    source: str
    target: str
    details: EdgeDetails


def create_graph_for_zone(idf: IDF, path_to_input: Path):
    G = nx.DiGraph()
    positions = {}
    room_map = create_room_map(path_to_input)

    # node should have num and label

    for ix, zone in enumerate(get_zones(idf)):
        room_name = room_map[ix]
        label = f"{ix}-{room_name}"
        G.add_node(label, num=ix, room_name=room_name, zone_name=zone.Name)
        positions[label] = create_domain_for_zone(idf, ix).create_centroid().pair
        # positions
    return G, positions


def add_cardinal_directions(G: nx.DiGraph, positions: NodePositions):
    for i in WallNormal:
        G.add_node(i.name, type="Direction")
    new_positions = create_cardinal_positions(positions)
    return G, new_positions


def filter_nodes(G: nx.DiGraph):
    zone_nodes = [i[0] for i in G.nodes(data=True) if "zone_name" in i[1].keys()]
    cardinal_nodes = [i[0] for i in G.nodes(data=True) if "type" in i[1].keys()]
    return zone_nodes, cardinal_nodes


def get_node_in_G(G, space: WallNormal | int):
    try:
        assert not isinstance(space, int)
        return space.name
    except:
        assert not hasattr(space, "name")
        for i, data in G.nodes(data=True):
            if "num" in data.keys():
                if data["num"] == space:
                    return i
        raise Exception("No matching node found")


def add_edges(idf: IDF, G: nx.DiGraph, pairs: list[SubsurfacePair]):
    for pair in pairs:
        surf = get_connecting_surface(idf, pair)
        assert surf
        subsurface = surf.subsurfaces[0]  # just one each
        node_a = get_node_in_G(G, pair.space_a)
        node_b = get_node_in_G(G, pair.space_b)
        G.add_edge(node_a, node_b, surface=surf.Name, subsurfaces=subsurface.Name, stype=pair.attrs.object_type.name)  # type: ignore

    return G

def create_base_graph(idf: IDF, path_to_input: Path):
    G, positions = create_graph_for_zone(idf, path_to_input)
    G, positions  = add_cardinal_directions(G, positions)
    pairs = get_subsurface_pairs_from_case(path_to_input)
    G = add_edges(idf, G, pairs)
    return G, positions

def get_subsurface_wall_num(name: str):
    temp = name.split(" ")[-2]
    res = temp.split("_")
    if len(res) == 1:
        return int(res[0])
    elif len(res) == 2:
        r = int(res[0])
        s = int(res[1])
        return float(f"{r}.{s}")
    else:
        raise Exception(f"Invalid name: {name}")



def create_edge_label(idf: IDF, G: nx.DiGraph, edge: GraphEdge):
    # TODO put elsewhere.. 
    def map_ss_type(val):
        d = {"DOOR": "DR", "WINDOW": "WND"}
        return d[val]

    def short_drn(name):
        assert str(name)
        return name[0]

    owning_zone = G.nodes[edge.source]["num"]
    type = map_ss_type(edge.details["stype"])
    wall_num = get_subsurface_wall_num(edge.details["subsurfaces"])
    # drn = get_surface_direction(idf, edge.details["surface"]).name
    # s_drn = short_drn(drn)

    return f"{type}-{owning_zone}-{wall_num}"

def create_edge_label_dict(idf: IDF, G: nx.DiGraph):
    nice_edges = [GraphEdge(*e) for e in G.edges(data=True)]
    return {(e.source, e.target):create_edge_label(idf, G, e) for e in nice_edges}


def create_afn_graph(idf: IDF, G: nx.DiGraph):
    def is_node_afn_zone(node):
        afn_zones = [i.Zone_Name for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]]
        return G.nodes[node].get("zone_name") in afn_zones

    def is_edge_afn_surface(e1, e2):
        afn_surfaces = [i.Surface_Name for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]]
        res = G.edges[(e1, e2)].get("subsurfaces") in afn_surfaces
        return res

    return nx.subgraph_view(G, filter_node=is_node_afn_zone), nx.subgraph_view(G, filter_edge=is_edge_afn_surface)