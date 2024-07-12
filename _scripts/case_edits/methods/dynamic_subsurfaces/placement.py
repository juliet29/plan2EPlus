from shapely import Point
from case_edits.methods.dynamic_subsurfaces.buffer import Buffer
from case_edits.methods.dynamic_subsurfaces.inputs import (
    Dimensions,
    NinePointsLocator,
    MutablePoint,
)

"""
From EP 22.2 Docs: Starting corner is the lower left of the surface 
https://bigladdersoftware.com/epx/docs/23-2/input-output-reference/group-thermal-zone-description-geometry.html#windowsdoors
"""


class Placement:
    def __init__(
        self,
        buffer_surface: Buffer,
        subsurface_dims: Dimensions,
        location: NinePointsLocator,
    ) -> None:
        # self.buffer_surface = buffer_surface
        self.surface_dims = buffer_surface.surface.dimensions
        self.pts = buffer_surface.nine_points
        self.dims = subsurface_dims
        self.loc = location
        self.starting_corner = MutablePoint(x=0, y=0)

        self.run_prelim_checks()
        self.find_starting_corner()

    def run_prelim_checks(self):
        assert self.dims.height < self.surface_dims.height
        assert self.dims.width < self.surface_dims.width

    def find_starting_corner(self):
        match self.loc.value:
            case 0:
                self.place_top_left()
            case 1:
                self.place_top_middle()
            case 2:
                self.place_top_right()
            case 3:
                self.place_middle_left()
            case 4:
                self.place_middle_middle()
            case 5:
                self.place_middle_right()
            case 6:
                self.place_bottom_left()
            case 7:
                self.place_bottom_middle()
            case 8:
                self.place_bottom_right()
            case _: 
                raise Exception("Invalid Case")


        
    def place_top_left(self):
        self.starting_corner = MutablePoint(self.pts.top_left)
        self.extend_down()

    def place_top_middle(self):
        self.starting_corner = MutablePoint(self.pts.top_middle)
        self.extend_down()
        self.extend_left_half()

    def place_top_right(self):
        self.starting_corner = MutablePoint(self.pts.top_right)
        self.extend_down()
        self.extend_left()


    def place_middle_left(self):
        self.starting_corner = MutablePoint(self.pts.middle_left)
        self.extend_down_half()

    def place_middle_middle(self):
        self.starting_corner = MutablePoint(self.pts.middle_middle)
        self.extend_down_half()
        self.extend_down()

    def place_middle_right(self):
        self.starting_corner = MutablePoint(self.pts.middle_right)
        self.extend_down_half()
        self.extend_left()


    def place_bottom_left(self):
        self.starting_corner = MutablePoint(self.pts.bottom_left)

    def place_bottom_middle(self):
        self.starting_corner = MutablePoint(self.pts.bottom_middle)
        self.extend_left_half()

    def place_bottom_right(self):
        self.starting_corner = MutablePoint(self.pts.bottom_right)
        self.extend_left()



    # TODO => check that extending does not break.. 
    



    def extend_down(self):
        val = self.starting_corner.y - self.dims.height
        self.starting_corner.update_vals(y=val)

    def extend_down_half(self):
        val = self.starting_corner.y - (self.dims.height / 2)
        self.starting_corner.update_vals(y=val)

    def extend_left(self):
        val = self.starting_corner.x - (self.dims.width)
        self.starting_corner.update_vals(x=val)

    def extend_left_half(self):
        val = self.starting_corner.x - (self.dims.width / 2)
        self.starting_corner.update_vals(x=val)
