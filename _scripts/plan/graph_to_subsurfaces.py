from pathlib import Path
import json
from helpers.helpers import key_from_value
from subsurfaces.interfaces import NinePointsLocator, SubsurfacePair
from geometry.wall_normal import WallNormal
from subsurfaces.interfaces import SubsurfaceAttributes, SubsurfaceObjects
from subsurfaces.interfaces import (
    Dimensions,
)
from plan.interfaces import (
    SubSurfacesJSON,
    WindowsJSON,
    DoorsJSON,
    DetailsJSON,
    GraphEdgeJSON,
    GRAPH,
    SUBSURFACES,
)
from plan.helpers import load_data_from_json, create_room_map


def get_dimensions(item: DoorsJSON | WindowsJSON):
    w, h = item["width"], item["height"]
    return Dimensions(float(w), float(h))


def create_subsurface_database(
    subsurfaces: SubSurfacesJSON,
    object_type: SubsurfaceObjects,
    location: NinePointsLocator,
):
    def create_attributes(item: DoorsJSON | WindowsJSON):
        return SubsurfaceAttributes(
            object_type=object_type,
            construction=None,
            dimensions=get_dimensions(item),
            location_in_wall=location,
        )

    ot = "WINDOWS" if object_type == SubsurfaceObjects.WINDOW else "DOORS"
    return {item["id"]: create_attributes(item) for item in subsurfaces[ot]}


def load_attributes(path_to_inputs: Path):
    # TODO handle type 0
    subsurfaces: SubSurfacesJSON = load_data_from_json(path_to_inputs, SUBSURFACES)
    doors_db = create_subsurface_database(
        subsurfaces, SubsurfaceObjects.DOOR, NinePointsLocator.bottom_middle
    )
    windows_db = create_subsurface_database(
        subsurfaces, SubsurfaceObjects.WINDOW, NinePointsLocator.top_middle
    )
    return [windows_db, doors_db]


def get_attr(details: DetailsJSON, databases: list[dict[int, SubsurfaceAttributes]]):
    windows_db, doors_db = databases
    if details["external"]:
        return windows_db[details["id"]]
    else:
        return doors_db[details["id"]]


def get_node_mapping(node: str, room_map: dict[int, str]):
    try:
        return key_from_value(room_map, node)
    except:
        return WallNormal[node]


def handle_edge(
    e: GraphEdgeJSON,
    room_map: dict[int, str],
    databases: list[dict[int, SubsurfaceAttributes]],
):
    source, target = sorted(
        [e["source"], e["target"]],
        key=lambda x: x not in room_map.values(),
    )
    return SubsurfacePair(
        key_from_value(room_map, source),
        get_node_mapping(target, room_map),
        get_attr(e["details"], databases),
    )


def get_subsurface_pairs_from_case(path_to_inputs: Path):
    room_map = create_room_map(path_to_inputs)
    databases = load_attributes(path_to_inputs)
    graph_data = load_data_from_json(path_to_inputs, GRAPH)
    edges: list[GraphEdgeJSON] = graph_data["links"]
    return [handle_edge(e, room_map, databases) for e in edges]
