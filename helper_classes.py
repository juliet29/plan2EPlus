import shapely as sp
from geomeppy.patches import EpBunch


class Zone:
    def __init__(self, idf_data:EpBunch) -> None:
        self.data = idf_data
        self.name = idf_data.Name
        self.walls:list[Wall] = []
        # TODO show names when printed.. 

    def __repr__(self):
        return f"Zone({self.name})"


class Wall:
    def __init__(self, idf_data:EpBunch) -> None:
        self.data = idf_data
        self.name = idf_data.Name
        # self.fieldnames = idf_data.fieldnames
        # self.fieldvalues = idf_data.fieldnames

        self.line:sp.LineString = None
        self.boundary_condition = None
    def __repr__(self):
        return f"Wall({self.name})"       
