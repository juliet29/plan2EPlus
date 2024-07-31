from shapely import Point, Polygon
import numpy as np
from methods.dynamic_subsurfaces.inputs import Dimensions
from helpers.shapely_helpers import get_coords_as_points, CoordOrganizer




class SurfacePolygon:
    def __init__(self, polygon:Polygon) -> None:
        self.polygon = polygon
        self.coord_sequence = self.polygon.exterior.coords
        self.coords = get_coords_as_points(self.polygon.exterior.coords)
        self.organized_coords = CoordOrganizer(self.polygon.exterior.coords)
        
        self.dimensions = Dimensions(0,0)
        self.auto_dimension()
        

    def auto_dimension(self):
        self.dimensions.width  = abs(self.organized_coords.x1 - self.organized_coords.x0)
        self.dimensions.height  =  abs(self.organized_coords.y1 - self.organized_coords.y0)

        # check 
        # try:
        #     assert self.polygon.area
        # except:
        #     "Invalid polygon"
        #     area_height = self.polygon.area / self.dimensions.width
        #     assert np.isclose(a=area_height, b=self.dimensions.height), f"area_height: {area_height}, dim_height: {self.dimensions.height} "
        # except:
        #     return self.organized_coords

    def update_dimensions(self, w, h):
        self.dimensions.width = w
        self.dimensions.height = h





    