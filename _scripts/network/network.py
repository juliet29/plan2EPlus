from pathlib import Path
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
from plan.helpers import create_room_map, get_plans_from_file


def create_subsurface_positions(coord: Coord, direction: WallNormal, diff=0.4):
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
    return int(temp.split("_")[0])


def get_subsurface_direction(idf, subsurface: EpBunch):
    s = get_surface_of_subsurface(idf, subsurface)
    assert s
    if s.azimuth not in [i.value for i in WallNormal]:
        print(subsurface.Name, s.azimuth)
    return WallNormal(round(s.azimuth))


def get_display_data_for_subsurface(idf, subsurface: EpBunch):
    direction = get_subsurface_direction(idf, subsurface)
    wall_num = get_subsurface_wall_num(subsurface.Name)
    ss_type = subsurface.Name.split(" ")[-1]
    return (ss_type, wall_num, direction)


def get_display_data_for_zone(path_to_input: Path, name: str):
    room_map = create_room_map(path_to_input)
    num = int(name.split(" ")[1])
    label = room_map[num]
    return num, label


def get_room_positions(path_to_input: Path):
    plans = get_plans_from_file(path_to_input)
    return [i.get_node_data() for i in plans]


def create_graph(idf: IDF, path_to_input: Path):
    zone_map = create_zone_map_without_partners(idf)
    room_positions = get_room_positions(path_to_input)
    G = nx.Graph()
    positions = {}

    for zone, subsurfaces in zone_map.items():
        num, label = get_display_data_for_zone(path_to_input, zone)
        zone_label = f"Z_{num}"
        G.add_node(zone_label, label=label, num=num, dtype="zone")
        positions[zone_label] = [i[-1] for i in room_positions if i[0] == num][0]

        for subsurface_name in subsurfaces:
            subsurface = get_subsurface_by_name(idf, subsurface_name)
            ss_type, wall_num, direction = get_display_data_for_subsurface(
                idf, subsurface
            )
            ss_label = f"SS_{num}-{wall_num}_{ss_type}"
            G.add_node(
                ss_label,
                ss_type=ss_type,
                wall_num=wall_num,
                direction=direction.name,
                dtype="subsurface",
            )
            G.add_edge(zone_label, ss_label)
            positions[ss_label] = create_subsurface_positions(
                positions[zone_label], direction
            )

    pos = {k: v.pair for k, v in positions.items()}
    return G, pos


# positions..
