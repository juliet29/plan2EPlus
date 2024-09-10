import os
import json

from methods.subsurfaces.pairs import SubsurfaceAttributes, SubsurfaceObjects
from methods.dynamic_subsurfaces.inputs import (
    Dimensions,
    NinePointsLocator,
)
from helpers.dimensions import nice_dim


DETAILS_PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/plan_details"


class AttributeCreator:
    def __init__(self, file_name: str = "amber_building.json") -> None:
        self.file_path = os.path.join(DETAILS_PATH, file_name)

    def run(self):
        self.get_data()
        self.create_windows()
        self.create_doors()

    def get_data(self):
        with open(self.file_path) as f:
            self.details = json.load(f)

    def create_windows(self):
        self.window_db = {}
        for item in self.details["WINDOW_TYPES"]:
            self.window_db[item["id"]] = SubsurfaceAttributes(
                object_type=SubsurfaceObjects.WINDOW,
                construction=None,
                dimensions=Dimensions(
                    nice_dim(item["width"]), nice_dim(item["height"])
                ),
                location_in_wall=NinePointsLocator.top_middle,
            )

    def create_doors(self):
        self.door_db = {}
        for item in self.details["DOOR_TYPES"]:
            self.door_db[item["id"]] = SubsurfaceAttributes(
                object_type=SubsurfaceObjects.DOOR,
                construction=None,
                dimensions=Dimensions(
                    nice_dim(item["width"]), nice_dim(item["height"])
                ),
                location_in_wall=NinePointsLocator.bottom_middle,
            )
