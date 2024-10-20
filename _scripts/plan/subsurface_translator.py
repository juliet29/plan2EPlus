from pathlib import Path
import json
from helpers.helpers import key_from_value
from new_subsurfaces.interfaces import NinePointsLocator, SubsurfacePair
from geometry.wall_normal import WallNormal
from new_subsurfaces.interfaces import SubsurfaceAttributes, SubsurfaceObjects
from plan.interfaces import DetailsJSON, GraphEdgeJSON, SubSurfacesJSON, RoomTypeJSON
from new_subsurfaces.interfaces import (
    Dimensions,
)
from plan.interfaces import (
    SubSurfacesJSON,
    WindowsJSON,
    DoorsJSON,
    GRAPH,
    PLAN,
    SUBSURFACES,
)

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


def get_dimensions(item: DoorsJSON | WindowsJSON):
    w, h = item["width"], item["height"]
    return Dimensions(float(w), float(h))


class SubsurfaceTranslator:
    def __init__(self, path_to_inputs: Path) -> None:
        self.pairs: list[SubsurfacePair] = []
        self.path_to_inputs = path_to_inputs

    def run(self):
        self.create_room_map()
        self.create_subsurfaces()

    def load_data_from_json(self, file_name):
        with open(self.path_to_inputs / file_name) as f:
            res = json.load(f)
        return res

    def create_room_map(self):
        # TODO make this accessible elsewhere.. 
        self.plan_data: list[list[RoomTypeJSON]] = self.load_data_from_json(PLAN)
        self.room_map = {}
        for item in self.plan_data[0]:
            self.room_map[item["id"]] = item["label"]

    def create_subsurfaces(self):
        self.graph_data = self.load_data_from_json(GRAPH)
        self.load_attributes()
        edges: list[GraphEdgeJSON] = self.graph_data["links"]
        for e in edges:
            source, target = sorted(
                [e["source"], e["target"]],
                key=lambda x: x not in self.room_map.values(),
            )
            self.pairs.append(
                SubsurfacePair(
                    key_from_value(self.room_map, source),
                    self.get_node_mapping(target),
                    self.get_attr(e["details"]),
                )
            )

    def load_attributes(self):
        # TODO handle type 0
        self.subsurfaces: SubSurfacesJSON = self.load_data_from_json(SUBSURFACES)
        self.doors_db = create_subsurface_database(
            self.subsurfaces, SubsurfaceObjects.DOOR, NinePointsLocator.bottom_middle
        )
        self.windows_db = create_subsurface_database(
            self.subsurfaces, SubsurfaceObjects.WINDOW, NinePointsLocator.top_middle
        )

    def get_attr(self, details: DetailsJSON):
        if details["external"]:
            return self.windows_db[details["id"]]
        else:
            return self.doors_db[details["id"]]

    def get_node_mapping(self, node):
        try:
            return key_from_value(self.room_map, node)
        except:
            return WallNormal[node]

def get_subsurface_pairs_from_case(path_to_inputs: Path):
    st = SubsurfaceTranslator(path_to_inputs)
    st.run()
    return st.pairs