from shapely.coords import CoordinateSequence
from shapely import Point


def get_point_as_xy(point: Point):
    return tuple([i[0] for i in point.xy])


def get_coords_as_seprate_xy(coords: CoordinateSequence):
    x = [c[0] for c in coords]
    y = [c[1] for c in coords]
    if len(coords[0]) == 3:
        z = [c[2] for c in coords]  # type: ignore
    else:
        z = [0]

    return x, y, z


def get_coords_as_points(coords: CoordinateSequence):
    return [Point(c) for c in coords]


def list_coords(coords: CoordinateSequence):
    return [c for c in coords]


class CoordOrganizer:
    # ref: https://plotly.com/python/reference/layout/shapes/#layout-shapes-items-shape-x0
    def __init__(self, coords: CoordinateSequence) -> None:
        self.coords = coords
        x, y, z = get_coords_as_seprate_xy(self.coords)
        self.x0 = min(x)
        self.x1 = max(x)
        self.y0 = min(y)
        self.y1 = max(y)
        self.z0 = min(z)
        self.z1 = max(z)

        self.identify_corners()

    def __repr__(self):
        return f"PlotCoords(({self.x0}, {self.y0}, {self.z0}), ({self.x1}, {self.y1}, {self.z1}))"

    def identify_corners(self):
        if len(self.coords) >= 4:
            if not self.is_same_in_z():
                self.transform_to_2D()
            self.bottom_left = Point(self.x0, self.y0)
            self.bottom_right = Point(self.x1, self.y0)
            self.top_right = Point(self.x1, self.y1)
            self.top_left = Point(self.x0, self.y1)

            self.coords_list = [
                self.bottom_left,
                self.bottom_right,
                self.top_right,
                self.top_left,
                self.bottom_left,
            ]

    def transform_to_2D(self):
        if self.is_same_in_x() and not self.is_same_in_y():
            self.transform_y_to_x()
            self.transform_z_to_y()
        elif not self.is_same_in_x() and self.is_same_in_y():
            self.transform_z_to_y()

    def transform_y_to_x(self):
        self.x0 = self.y0
        self.x1 = self.y1

    def transform_z_to_y(self):
        self.y0 = self.z0
        self.y1 = self.z1
        self.z0 = self.z1 = 0

    def is_same_in_y(self):
        if self.y0 == self.y1:
            return True

    def is_same_in_x(self):
        if self.x0 == self.x1:
            return True

    def is_same_in_z(self):
        if self.z0 == self.z1:
            return True
