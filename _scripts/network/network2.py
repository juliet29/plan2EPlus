# plot nodes and labels..
from pathlib import Path
from typing import Optional
from geomeppy import IDF

import networkx as nx
from network.cardinal_positions import create_cardinal_positions, NodePositions
from plan.helpers import create_room_map
from helpers.ep_helpers import get_zones, WallNormal
from helpers.ep_geom_helpers import create_domain_for_zone
from subsurfaces.interfaces import SubsurfacePair
from subsurfaces.logic import get_connecting_surface


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
    nodes = list(G.nodes)
    try:
        assert not isinstance(space, int)
        return space.name
    except:
        assert not hasattr(space, "name")
        for i in nodes:
            if int(i[0]) == space:
                return i
        raise Exception("No matching node found")

def add_edges(idf: IDF, G: nx.DiGraph, pairs: list[SubsurfacePair]):
    for pair in pairs:
        surf = get_connecting_surface(idf, pair)
        assert surf
        subsurface = surf.subsurfaces[0] #just one each
        node_a = get_node_in_G(G, pair.space_a)
        node_b = get_node_in_G(G, pair.space_b)
        G.add_edge(node_a, node_b, surface=surf.Name, subsurfaces=subsurface, stype=pair.attrs.object_type.name)

    return G

