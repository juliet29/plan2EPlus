# assuming meters?
import json
from typing import List, Union
from gplan.room_class import GPLANRoomType, GPLANRoomAccess
from gplan.room import GPLANRoom


class GPLANtoGeomeppy:
    def __init__(
        self,
        case,
        geometry: Union[List[GPLANRoomType], GPLANRoomAccess],
    ) -> None:
        self.case = case
        self.geometry = geometry

        self.blocks = []

        self.run()


    def run(self):
        self.get_plans()
        self.create_blocks()
        self.adjust_blocks_y()
        self.update_case()


    def get_plans(self):
        if type(self.geometry) == GPLANRoomAccess:
            self.gplan_access = self.geometry
            self.get_plans_from_file()
        else:
            self.plan = self.geometry

        

    def get_plans_from_file(self):
        with open(self.gplan_access.path) as f:
            gplan_data = json.load(f)
        self.plan = gplan_data[self.gplan_access.index]


    def create_blocks(self):
        assert type(self.plan) == list
        for block in self.plan:
            g = GPLANRoom(block)
            self.blocks.append(g.eppy_block)


    def adjust_blocks_y(self):
        # get the most negative y value 
        ys = []
        for block in self.blocks:
            for coord in block["coordinates"]:
                ys.append(abs(coord[1]))
        y_max = max(ys)
        # move all blocks up by this amount 
        for block in self.blocks:
            block["coordinates"] = [(coord[0], coord[1]+y_max) for coord in block["coordinates"]]


    def update_case(self):
        for block in self.blocks:
            self.case.idf.add_block(**block)
