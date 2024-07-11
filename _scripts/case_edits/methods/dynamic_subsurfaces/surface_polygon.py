from shapely import Point, Polygon
from dataclasses import dataclass
import numpy as np

from helpers.shapely_helpers import get_coords_as_points


@dataclass
class Dimensions:
    width: float
    height: float


class SurfacePolygon:
    def __init__(self, polygon:Polygon) -> None:
        self.polygon = polygon
        self.coords = get_coords_as_points(self.polygon.exterior.coords)
        
        self.dimensions = Dimensions(0,0)
        self.auto_dimension()
        

    def auto_dimension(self):
        # TODO CHECK THAT GOING CCW..
        self.dimensions.width  = self.coords[1].x - self.coords[0].x
        self.dimensions.height  =  self.coords[2].y - self.coords[0].y

        # check 
        area_height = self.polygon.area / self.dimensions.width
        assert np.isclose(a=area_height, b=self.dimensions.height), f"area_height: {area_height}, dim_height: {self.dimensions.height} "

    def update_dimensions(self, w, h):
        self.dimensions.width = w
        self.dimensions.height = h





    