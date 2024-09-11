from dataclasses import dataclass
import os
import json
from helpers.helpers import key_from_value
from methods.subsurfaces.pairs import  SubsurfacePair, SubsurfaceObjects
from gplan.attribute_creator import AttributeCreator
from geometry.wall_normal import WallNormal


GRAPH_JSON = "graph.json"
GPLAN_JSON = "gplan.json"
OUTPUTS_PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/outputs"

class SubsurfaceTranslator:
    def __init__(self, folder_name: str) -> None:
        self.folder_path = os.path.join(OUTPUTS_PATH, folder_name)
        self.pairs: list[SubsurfacePair] = []

    def run(self):
        self.get_data()
        self.create_room_map()
        self.create_subsurfaces()

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


    def create_subsurfaces(self):
        self.load_attributes()
        edges = self.graph_data["links"]
        for e in edges:
            data = e["data"]
            source = key_from_value(self.room_map, e["source"])
            assert source + 1
            try:
                target = key_from_value(self.room_map, e["target"])
            except:
                target = WallNormal[e["target"]]

            self.pairs.append(
                SubsurfacePair(
                    source,
                    target,
                    self.get_attr(data["door_or_window"], data["id"]),
                )
            )

    def load_attributes(self):
        self.ac = AttributeCreator()
        self.ac.run()


    def get_attr(self, obj_type, id):
        if obj_type == SubsurfaceObjects.DOOR.name:
            db = self.ac.door_db
        elif obj_type == SubsurfaceObjects.WINDOW.name:
            db = self.ac.window_db
        else:
            raise Exception("wrong object type")
        
        try:
            return db[str(id)]
        except:
            return db[id]
