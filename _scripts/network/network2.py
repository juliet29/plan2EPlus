# plot nodes and labels..
from copy import deepcopy
from pathlib import Path
from typing import Optional
from geomeppy import IDF

import networkx as nx
from plan.helpers import create_room_map
from helpers.ep_helpers import get_zones, WallNormal
from helpers.ep_geom_helpers import create_domain_for_zone
from helpers.geometry_interfaces import Domain, Range

NodePositions = dict[str, tuple[float, float]]

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


# zone_nodes = [i for i in G.nodes(data=True) if i[1]["zone_name"]]


# add cardinal positions..


def get_bounds_of_positioned_graph(pos: NodePositions):
    x_values = [coord[0] for coord in pos.values()]
    y_values = [coord[1] for coord in pos.values()]

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    return Domain(Range(x_min, x_max), Range(y_min, y_max))


def create_cardinal_positions(_positions: NodePositions, PAD=1):
    positions = deepcopy(_positions)
    c = get_bounds_of_positioned_graph(positions)
    mid_x = c.width.midpoint() 
    mid_y = c.height.midpoint() 

    res = [
        (mid_x, c.height.max + PAD),
        (mid_x, c.height.min - PAD),
        (c.width.min - PAD, mid_y),
        (c.width.max + PAD, mid_y),
    ]

    drns = [WallNormal.NORTH, WallNormal.SOUTH, WallNormal.EAST, WallNormal.WEST]
    temp = {i.name: r for i, r in zip(drns, res)}
    
    positions.update(temp)
    return positions

def add_cardinal_directions(G: nx.DiGraph, positions: NodePositions):
    for i in WallNormal:
        G.add_node(i.name, type="Direction")
    new_positions = create_cardinal_positions(positions)
    return G, new_positions