from shapely.coords import CoordinateSequence
from shapely import Point

def get_coords_as_seprate_xy(coords: CoordinateSequence):
    x = [c[0] for c in coords]
    y = [c[1] for c in coords]
    return x, y


def get_coords_as_points(coords: CoordinateSequence):
    return [Point(c) for c in coords]