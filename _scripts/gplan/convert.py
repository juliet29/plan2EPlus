# assuming meters? 

class GPLANRoom:
    def __init__(self, block:dict, room_height=10) -> None:
         #TODO check that is #
        index = block["label"]
        self.name = f"0{index}"
        self.room_height = room_height

        self.xo = block["left"]
        self.yo = block["top"]
        self.width = block["width"]
        self.height = block["height"]

        self.create_geomeppy_block()

    def create_geomeppy_block(self):
        self.create_pos()
        self.create_coords()
        self.create_object()
        

    def create_pos(self):
        self.bottom_y = self.yo - self.height
        self.right_x = self.xo + self.width

        self.top_left = (self.xo, self.yo)
        self.top_right = (self.right_x, self.yo)

        self.bottom_left = (self.xo, self.bottom_y)
        self.bottom_right = (self.right_x, self.bottom_y)

    def create_coords(self):
        # positions in geomeppy block are arranged counter clockwise starting from the bottom right corner
        self.coords = [self.bottom_right, self.top_right, self.top_left, self.bottom_left]

    def create_object(self):
        self.eppy_block = {
            "name": self.name,
            "coordinates": self.coords,
            "height": self.room_height
        }




class GPLANtoGeomeppyBlock:
    # takes in a single room in the floor plan for now....
    def __init__(self, plan:list) -> None:
        self.plan = plan
        self.blocks = []
        
        self.create_blocks()

    def create_blocks(self):
        for block in self.plan:
            g = GPLANRoom(block) 
            self.blocks.append(g.eppy_block)





    
