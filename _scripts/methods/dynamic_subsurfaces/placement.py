from geomeppy.patches import EpBunch
from shapely import Point, Polygon
from methods.dynamic_subsurfaces.buffer import Buffer
from methods.dynamic_subsurfaces.inputs import (
    MutablePoint,
)

from methods.dynamic_subsurfaces.surface_polygon import SurfacePolygon
from helpers.plots import prepare_shape_dict, plot_shape, create_range_limits

from icecream import ic

from new_subsurfaces.interfaces import Dimensions
from new_subsurfaces.interfaces import Dimensions, NinePointsLocator
from helpers.ep_helpers import create_domain_for_rectangular_wall
from new_subsurfaces.placement import create_nine_points_for_domain


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
        FRACTION: bool = False,
    ) -> None:
        self.buffer_surface = buffer_surface
        self.bpts = buffer_surface.nine_points
        self.entered_dims = subsurface_dims
        self.loc = location
        self.FRACTION = FRACTION
        self.starting_corner = MutablePoint(x=0, y=0)

        self.run()

    def run(self):
        self.process_fraction()
        if self.run_prelim_checks():
            self.find_starting_corner()
            self.create_test_polygon()
            self.get_relative_starting_point()
        else:
            return False

    def process_fraction(self):
        if self.FRACTION:
            self.dims = Dimensions(0, 0)
            self.dims.width = (
                self.entered_dims.width * self.buffer_surface.polygon.dimensions.width
            )
            self.dims.height = (
                self.entered_dims.height * self.buffer_surface.polygon.dimensions.height
            )
        else:
            self.dims = self.entered_dims

    def run_prelim_checks(self):
        try:
            assert self.dims.height < self.buffer_surface.polygon.dimensions.height
            assert self.dims.width < self.buffer_surface.polygon.dimensions.width
            return True

        except:
            print(
                f"ssurface: {self.dims.width, self.dims.height}. buffer surface: {self.buffer_surface.polygon.dimensions.width, self.buffer_surface.polygon.dimensions.height}"
            )
            print(
                f"original wall width: {self.buffer_surface.original_surface.dimensions.width}"
            )
            raise Exception("ssurfaced dims > surface dims")

    def get_relative_starting_point(self):
        org_coords = self.buffer_surface.original_surface.organized_coords
        self.relative_x = abs(org_coords.x0 - self.starting_corner.x)
        self.relative_y = abs(org_coords.y0 - self.starting_corner.y)

        if (
            self.relative_x != self.starting_corner.x
            or self.relative_y != self.starting_corner.y
        ):
            self.old_starting_corner = self.starting_corner
            self.starting_corner = MutablePoint(x=self.relative_x, y=self.relative_y)

    def create_test_polygon(self):
        x0 = self.starting_corner.x
        y0 = self.starting_corner.y
        bottom_left = (x0, y0)
        bottom_right = (x0 + self.dims.width, y0)
        top_right = (x0 + self.dims.width, y0 + self.dims.height)
        top_left = (x0, y0 + self.dims.height)

        polygon = Polygon([bottom_left, bottom_right, top_right, top_left, bottom_left])
        self.polygon = SurfacePolygon(polygon)

        assert (
            self.buffer_surface.polygon.polygon.crosses(self.polygon.polygon) == False
        )

    def plot_test(self):
        self.buffer_trace = prepare_shape_dict(
            self.buffer_surface.polygon.coord_sequence
        )
        self.window_trace = prepare_shape_dict(
            self.polygon.coord_sequence, color="yellow"
        )

        traces = {i: v for i, v in enumerate([self.buffer_trace, self.window_trace])}

        xrange, yrange = create_range_limits(self.buffer_trace)

        fig = plot_shape(traces, xrange, yrange)
        fig.show()

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
        self.starting_corner = MutablePoint(self.bpts.top_left)
        self.extend_down()

    def place_top_middle(self):
        self.starting_corner = MutablePoint(self.bpts.top_middle)
        self.extend_down()
        self.extend_left_half()

    def place_top_right(self):
        self.starting_corner = MutablePoint(self.bpts.top_right)
        self.extend_down()
        self.extend_left()

    def place_middle_left(self):
        self.starting_corner = MutablePoint(self.bpts.middle_left)
        self.extend_down_half()

    def place_middle_middle(self):
        self.starting_corner = MutablePoint(self.bpts.middle_middle)
        self.extend_down_half()
        self.extend_left_half()

    def place_middle_right(self):
        self.starting_corner = MutablePoint(self.bpts.middle_right)
        self.extend_down_half()
        self.extend_left()

    def place_bottom_left(self):
        self.starting_corner = MutablePoint(self.bpts.bottom_left)

    def place_bottom_middle(self):
        self.starting_corner = MutablePoint(self.bpts.bottom_middle)
        self.extend_left_half()

    def place_bottom_right(self):
        self.starting_corner = MutablePoint(self.bpts.bottom_right)
        self.extend_left()

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


def create_starting_coord(surface: EpBunch, dim: Dimensions, loc: str):
    domain = create_domain_for_rectangular_wall(surface)
    np_dict = create_nine_points_for_domain(domain)
    placement_details = np_dict[loc]
    init_coord = placement_details.point
    for fx in placement_details.functions:
        new_coord = fx(init_coord, dim)
    return new_coord
