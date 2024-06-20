from gplan.room_type import GPLANRoomType
from icecream import ic

class GPLANRoom:
    def __init__(self, block: GPLANRoomType, room_height=10) -> None:
        index = block["label"]  # TODO check that is label is a #
        self.name = f"0{index}"
        self.room_height = room_height

        self.left_x = block["left"]
        self.top_y = block["top"]
        self.width = block["width"]
        self.height = block["height"]

        self.create_geomeppy_block()

    def create_geomeppy_block(self):
        self.create_pos()
        self.create_coords()
        # self.flip_coords()
        self.create_object()

    # def create_pos0(self):
    #     self.toptop_y = self.top_y + self.height
    #     self.right_x = self.left_x + self.width

    #     self.bottom_left = (self.left_x, self.top_y)
    #     self.bottom_right = (self.right_x, self.top_y)

    #     self.top_left = (self.left_x, self.toptop_y)
    #     self.top_right = (self.right_x, self.toptop_y)

    def create_pos(self):
        # using a convention where blocks are added from x=0, then going down.. 
        self.top_y*=-1
        self.bottom_y = self.top_y - self.height
        self.right_x = self.left_x + self.width

        self.bottom_left = (self.left_x, self.bottom_y)
        self.bottom_right = (self.right_x, self.bottom_y)

        self.top_left = (self.left_x, self.top_y)
        self.top_right = (self.right_x, self.top_y)

        # if self.name == "01":
        #     ic((self.left_x, self.top_y))


    def create_coords(self):
        # positions in geomeppy block are arranged counter clockwise starting from the bottom right corner. Search `geomeppy_block_entry.png` in Obsidian Vault
        self.coords = [
            self.bottom_right,
            self.top_right,
            self.top_left,
            self.bottom_left,
        ]

    # def flip_coords(self):
    #     y_mag = max([abs(pt[1]) for pt in self.coords])
    #     ic(y_mag)


    #     self.flipped_coords = [(pt[0], pt[1]+ y_mag) for pt in self.coords]
    #     ic(self.flipped_coords)

    def create_object(self):
        self.eppy_block = {
            "name": self.name,
            "coordinates":  self.coords, 
            "height": self.room_height,
        }
