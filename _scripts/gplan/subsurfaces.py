from dataclasses import dataclass
import os
import json
from typing import Union
from geometry.wall_normal import WallNormal
from helpers.helpers import key_from_value
from methods.subsurfaces.pairs import DEFAULT_WINDOW, SubsurfacePair, DEFAULT_DOOR


GRAPH_JSON = "graph.json"
GPLAN_JSON = "gplan.json"
FOLDER_PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/outputs"


@dataclass
class InputObject:
    node: Union[str, int]
    direction: str
    object_type: str


class SubsurfaceTranslator:
    def __init__(self, folder_name: str) -> None:
        self.folder_path = os.path.join(FOLDER_PATH, folder_name)
        self.door_pairs: list[SubsurfacePair] = []
        self.window_objects: list[InputObject] = []
        self.window_pairs: list[SubsurfacePair] = []

    def run(self):
        self.get_data()
        self.create_room_map()
        self.create_doors()
        self.create_windows()

    def get_data(self):
        self.gplan_path = os.path.join(self.folder_path, GPLAN_JSON)
        self.graph_path = os.path.join(self.folder_path, GRAPH_JSON)
        with open(self.gplan_path) as f:
            self.plan_data = json.load(f)
        with open(self.graph_path) as f:
            self.graph_data = json.load(f)

    def create_room_map(self):
        self.room_map = {}
        for item in self.plan_data[0]:
            self.room_map[item["id"]] = item["label"]

    def create_doors(self):
        doors = self.graph_data["links"]
        for item in doors:
            self.door_pairs.append(
                SubsurfacePair(
                    key_from_value(self.room_map, item["source"]),
                    key_from_value(self.room_map, item["target"]),
                    DEFAULT_DOOR,
                )
            )

    def create_windows(self):
        self.prepare_windows()
        for o in self.window_objects:
            node = key_from_value(self.room_map, o.node)
            direction = WallNormal[str(o.direction)]
            if o.object_type == "A":
                object_type = DEFAULT_WINDOW
            self.window_pairs.append(SubsurfacePair(node, direction, object_type))

    def prepare_windows(self):
        for node in self.graph_data["nodes"]:
            for w in node["windows"]:
                self.window_objects.append(
                    InputObject(node["id"], w["direction"], w["window_type"])
                )
