from pathlib import Path

from ..helpers.ep_helpers import WallNormal
from ..helpers.helpers import key_from_value
from ..subsurfaces.interfaces import (
    Dimensions,
    NinePointsLocator,
    SubsurfaceAttributes,
    SubsurfaceObjects,
    SubsurfacePair,
)
from .helpers import create_room_map, load_data_from_json
from .interfaces import (
    GRAPH,
    SUBSURFACES,
    DetailsJSON,
    DoorsJSON,
    GraphEdgeJSON,
    SubSurfacesJSON,
    WindowChangeData,
    WindowsJSON,
)


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
    except KeyError:
        return WallNormal[node]


def handle_edge(
    e: GraphEdgeJSON,
    room_map: dict[int, str],
    databases: list[dict[int, SubsurfaceAttributes]],
):
    source, target = e["source"], e["target"]
    return SubsurfacePair(
        get_node_mapping(source, room_map),
        get_node_mapping(target, room_map),
        get_attr(e["details"], databases),
    )


def modify_window_database(
    databases: list[dict[int, SubsurfaceAttributes]], value: float
):
    windows_db = databases[0]
    # print(windows_db)
    for attrs in windows_db.values():
        # TODO WindowChange Data name needs to be more expressive.. 
        attrs.dimensions = attrs.dimensions.modify_area(value)
    # print(windows_db)
    return databases


def get_subsurface_pairs_from_case(
    path_to_inputs: Path, win_change_data: WindowChangeData | None = None
) -> list[SubsurfacePair]:
    room_map = create_room_map(path_to_inputs)
    databases = load_attributes(path_to_inputs)

    if win_change_data: # TODO => fix this with modifications config.. goal is to parametrically alter window sizes.. 
        databases = modify_window_database(databases, win_change_data.value)

    graph_data = load_data_from_json(path_to_inputs, GRAPH)
    edges: list[GraphEdgeJSON] = graph_data["links"]
    return [
        handle_edge(e, room_map, databases) for e in edges if e["details"]["id"] != 0
    ]
