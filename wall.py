from helpers import *

class Wall:
    def __init__(self, idf_data:EpBunch) -> None:
        self.data = idf_data
        self.name = idf_data.Name
        # self.fieldnames = idf_data.fieldnames
        # self.fieldvalues = idf_data.fieldnames

        self.line:sp.LineString = None
        self.boundary_condition = None

        self.get_wall_geometry()


    def __repr__(self):
        return f"Wall({self.name})"    

    def get_wall_geometry(self,):
        z_coords = fnmatch.filter(self.data.fieldnames, "Vertex_[0-4]_Zcoordinate")

        # Define the regex pattern to match digits
        pattern = re.compile(r"\d+")

        vertices = []
        for fieldname in z_coords:
            if self.data[fieldname] == 0:
                # get the vertex number where z-coord is 0
                matches = pattern.findall(fieldname)
                # TODO some tests needed here..
                x_field = fnmatch.filter(
                    self.data.fieldnames, f"Vertex_{matches[0]}_Xcoordinate"
                )[0]
                x_val = self.data[x_field]

                y_field = fnmatch.filter(
                    self.data.fieldnames, f"Vertex_{matches[0]}_Ycoordinate"
                )[0]
                y_val = self.data[y_field]

                vertices.append([x_val, y_val])

        self.line = sp.LineString(vertices)