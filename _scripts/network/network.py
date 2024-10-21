from pathlib import Path
from turtle import position
from typing import Any, NamedTuple
from geomeppy import IDF
import networkx as nx
from helpers.ep_helpers import (
    EpBunch,
    WallNormal,
    create_zone_map,
    create_zone_map_without_partners,
    get_surface_of_subsurface,
    get_subsurface_by_name,
)
from helpers.geometry_interfaces import Coord
from plan.interfaces import RoomCoordinates
from plan.helpers import create_room_map, get_plans_from_file


def create_subsurface_positions(coord: Coord, direction: WallNormal, diff=0.3):
    match direction:
        case WallNormal.NORTH:
            return Coord(coord.x, coord.y + diff)
        case WallNormal.SOUTH:
            return Coord(coord.x, coord.y - diff)
        case WallNormal.EAST:
            return Coord(coord.x + diff, coord.y)
        case WallNormal.WEST:
            return Coord(coord.x - diff, coord.y)


# display data
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


def get_subsurface_direction(idf, subsurface: EpBunch):
    s = get_surface_of_subsurface(idf, subsurface)
    assert s
    if s.azimuth not in [i.value for i in WallNormal]:
        print(subsurface.Name, s.azimuth)
    return WallNormal(round(s.azimuth))


def get_display_data_for_subsurface(idf, subsurface: EpBunch):
    direction = get_subsurface_direction(idf, subsurface)
    wall_num = get_subsurface_wall_num(subsurface.Name)
    zone_num = int(subsurface.Name.split(" ")[1])
    ss_type = subsurface.Name.split(" ")[-1]
    return (ss_type, zone_num, wall_num, direction)


def get_display_data_for_zone(room_map: dict[int, str], name: str):
    num = int(name.split(" ")[1])
    label = room_map[num]
    return num, label


def get_room_positions(path_to_input: Path):
    plans = get_plans_from_file(path_to_input)
    return [i.get_coordinates() for i in plans]


class NodeData(NamedTuple):
    node_label: str
    data: dict[str, Any]
    position: Coord


def create_node_for_zone(
    room_posistions: list[RoomCoordinates], room_map: dict[int, str], zone: str
):
    def get_zone_coordinate(zone_num: int):
        return [i.coords for i in room_posistions if i.id == zone_num][0]

    num, label = get_display_data_for_zone(room_map, zone)
    zone_label = f"Z{num}"
    data = {"label": label, "zone_num": num, "dtype": "zone"}
    position = get_zone_coordinate(num)
    return NodeData(zone_label, data, position)


def create_node_for_subsurface(idf: IDF, subsurface_name: str, zone_data: NodeData):
    subsurface = get_subsurface_by_name(idf, subsurface_name)
    ss_type, zone_num, wall_num, direction = get_display_data_for_subsurface(
        idf, subsurface
    )

    def map_ss_type():
        d = {"Door": "DR", "Window": "WND"}
        return d[ss_type]

    ss_label = f"{zone_num}-{wall_num}_{map_ss_type()}"
    data = {
        "ss_type": ss_type,
        "wall_num": wall_num,
        "direction": direction.name,
        "dtype": "subsurface",
    }
    position = create_subsurface_positions(zone_data.position, direction)
    return NodeData(ss_label, data, position)


def update_node(G: nx.Graph, positions: dict, ndata: NodeData):
    G.add_node(ndata.node_label, data=ndata.data)
    positions[ndata.node_label] = ndata.position
    return G, positions


def create_graph_nodes(idf: IDF, path_to_input: Path):
    zone_map = create_zone_map_without_partners(idf)
    room_positions = get_room_positions(path_to_input)
    room_map = create_room_map(path_to_input)
    G = nx.DiGraph()
    edge_map = {}
    positions = {}

    for zone, subsurfaces in zone_map.items():
        zone_data = create_node_for_zone(room_positions, room_map, zone)
        edge_map[zone_data.node_label] = []
        G, positions = update_node(G, positions, zone_data)

        for subsurface_name in subsurfaces:
            ss_data = create_node_for_subsurface(idf, subsurface_name, zone_data)
            edge_map[zone_data.node_label].append(ss_data.node_label)
            G, positions = update_node(G, positions, ss_data)

    pos = {k: v.pair for k, v in positions.items()}
    return G, pos, edge_map


def update_graph_edges(G: nx.Graph, edge_map: dict):
    for k, v in edge_map.items():
        for ss in v:
            G.add_edge(k, ss)
    return G, edge_map


def create_graph(idf: IDF, path_to_input: Path):
    G, pos, edge_map = create_graph_nodes(idf, path_to_input)
    G, edge_map = update_graph_edges(G, edge_map)
    return G, pos, edge_map


# positions..
