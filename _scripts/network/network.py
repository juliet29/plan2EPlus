# plot nodes and labels..
from pathlib import Path
from typing import Optional
from geomeppy import IDF

import networkx as nx
from helpers.ep_helpers import get_subsurface_wall_num
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
        for node_name, data in G.nodes(data=True):
            if "num" in data.keys():
                if data["num"] == space:
                    return node_name
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
    G, positions = add_cardinal_directions(G, positions)
    pairs = get_subsurface_pairs_from_case(path_to_input)
    G = add_edges(idf, G, pairs)
    return G, positions


## TODO -- this goes elsewhere -------


def create_edge_label(G: nx.DiGraph, edge: GraphEdge):
    def map_ss_type(val):
        d = {"DOOR": "DR", "WINDOW": "WND"}
        return d[val]

    owning_zone = G.nodes[edge.source]["num"]
    type = map_ss_type(edge.details["stype"])
    wall_num = get_subsurface_wall_num(edge.details["subsurfaces"])

    return f"{type}-{owning_zone}-{wall_num}"


def create_edge_label_dict(G: nx.DiGraph):
    nice_edges = [GraphEdge(*e) for e in G.edges(data=True)]
    return {(e.source, e.target): create_edge_label(G, e) for e in nice_edges}


## -- ^^^ this goes elsewhere -------


def create_multi_graph(G: nx.DiGraph):
    G_rev = G.reverse()
    for e in G_rev.edges:
        G_rev.edges[e]["reverse"] = True
    Gm = nx.MultiDiGraph()
    Gm.add_edges_from(G.edges(data=True))
    Gm.add_edges_from(G_rev.edges(data=True))

    return Gm



def create_afn_graph(idf: IDF, G: nx.DiGraph):
    def is_node_afn_zone(node):
        afn_zones = [
            i.Zone_Name for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]
        ]
        return G.nodes[node].get("zone_name") in afn_zones

    def is_edge_afn_surface(e):
        afn_surfaces = [
            i.Surface_Name for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
        ]
        return G.edges[e].get("subsurfaces") in afn_surfaces

    nodes = [n for n in G.nodes if is_node_afn_zone(n)]
    G_zones = nx.subgraph(G, nodes)

    edges = [e for e in G.edges if is_edge_afn_surface(e)]
    G_afn = nx.edge_subgraph(G, edges)

    assert (
        G_zones.nodes < G_afn.nodes
    ), "Graph induced on subsurfaces should include all AFN zones"

    return G_afn


