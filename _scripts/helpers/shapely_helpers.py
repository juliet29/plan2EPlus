from shapely.coords import CoordinateSequence
from shapely import Point


class CoordOrganizer:
    # ref: https://plotly.com/python/reference/layout/shapes/#layout-shapes-items-shape-x0
    def __init__(self, coords: CoordinateSequence) -> None:
        self.coords = coords
        x, y = get_coords_as_seprate_xy(self.coords)
        self.x0 = min(x)
        self.x1 = max(x)
        self.y0 = min(y)
        self.y1 = max(y)

        self.identify_corners()

    def __repr__(self):
        return f"PlotCoords(({self.x0}, {self.y0}), ({self.x1}, {self.y1}))"

    def identify_corners(self):
        if len(self.coords) >= 4:
            self.bottom_left = Point(self.x0, self.y0)
            self.bottom_right = Point(self.x1, self.y0)
            self.top_right = Point(self.x1, self.y1)
            self.top_left = Point(self.x0, self.y1)

            self.coords_list = [self.bottom_left, self.bottom_right, self.top_right, self.top_left, self.bottom_left]


def get_coords_as_seprate_xy(coords: CoordinateSequence):
    x = [c[0] for c in coords]
    y = [c[1] for c in coords]
    return x, y


def get_coords_as_points(coords: CoordinateSequence):
    return [Point(c) for c in coords]
