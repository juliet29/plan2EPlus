from plan.room_class import GPLANRoomType
from icecream import ic
from decimal import Decimal

ROUNDING_LIM = 2


class GPLANRoom:
    def __init__(self, block: GPLANRoomType, room_height=10) -> None:
        self.block = block
        self.room_height = room_height


        self.create_geomeppy_block()

    def create_geomeppy_block(self):
        self.get_block_values()
        self.create_numeric_name()
        self.create_pos()
        self.create_coords()
        self.create_object()


    def get_block_values(self):
        self.left_x = self.get_block_value("left")
        self.top_y = self.get_block_value("top")
        self.width = self.get_block_value("width")
        self.height = self.get_block_value("height")


    def get_block_value(self, val):
        return Decimal(self.block[val])

    def create_numeric_name(self):
        label = self.block["label"]
        id  = self.block["id"]
        try:
            label = int(label) + 0
            self.name = f"0{label}"
        except ValueError:
            self.name = f"0{id}"

   






    def create_pos(self):
        # using a convention where blocks are added from y=0, then going down.. 
        self.top_y*=-1
        self.bottom_y = self.top_y - self.height
        self.right_x = self.left_x + self.width

        self.bottom_left = (self.left_x, self.bottom_y)
        self.bottom_right = (self.right_x, self.bottom_y)

        self.top_left = (self.left_x, self.top_y)
        self.top_right = (self.right_x, self.top_y)




    def create_coords(self):
        # positions in geomeppy block are arranged counter clockwise starting from the bottom right corner. Search `geomeppy_block_entry.png` in Obsidian Vault
        self.coords = [
            self.bottom_right,
            self.top_right,
            self.top_left,
            self.bottom_left,
        ]


    def create_object(self):
        self.eppy_block = {
            "name": self.name,
            "coordinates":  self.coords, 
            "height": self.room_height,
        }
