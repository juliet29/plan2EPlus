from matplotlib.patches import Rectangle
from dataclasses import dataclass
from plan2eplus.geometry.coords import Bounds, Coord, PerimeterMidpoints
from plan2eplus.geometry.range import Range


def extend_bounds(bounds: Bounds, EXTENTS: int):
    br = (bounds.br.x + EXTENTS, bounds.br.y - EXTENTS)
    tr = (bounds.tr.x + EXTENTS, bounds.tr.y + EXTENTS)
    tl = (bounds.tl.x - EXTENTS, bounds.tl.y + EXTENTS)
    bl = (bounds.bl.x - EXTENTS), bounds.bl.y - EXTENTS
    coords = [br, tr, tl, bl]
    return Bounds(*[Coord(*i) for i in coords])


@dataclass(frozen=True)
class Domain:
    horz_range: Range
    vert_range: Range

    @classmethod
    def from_coords_list(cls, coords: list[Coord]):
        # TODO can it be > 4 coords?
        xs = sorted(set([i.x for i in coords]))
        ys = sorted(set([i.y for i in coords]))
        horz_range = Range(xs[0], xs[-1])
        vert_range = Range(ys[0], ys[-1])
        return cls(horz_range, vert_range)

    @classmethod
    def from_perimeter_mid_points(cls, pm: PerimeterMidpoints):
        horz_range = Range(pm.WEST.x, pm.EAST.x)
        vert_range = Range(pm.SOUTH.y, pm.NORTH.y)
        return cls(horz_range, vert_range)

    @classmethod
    def from_bounds(cls, bounds: Bounds):
        horz_range = Range(bounds.tl.x, bounds.tr.x)
        vert_range = Range(bounds.bl.y, bounds.tl.y)
        return cls(horz_range, vert_range)

    @property
    def centroid(self):
        return Coord(self.horz_range.midpoint, self.vert_range.midpoint)

    @property
    def area(self):
        return self.horz_range.size * self.vert_range.size

    @property
    def aspect_ratio(self):
        return self.horz_range.size / self.vert_range.size

    def create_bounds(self, EXTENTS=0):  # TODO should be a property..
        # following requirements for geomeppy block
        # ccw from bottom right
        br = (self.horz_range.max, self.vert_range.min)
        tr = (self.horz_range.max, self.vert_range.max)
        tl = (self.horz_range.min, self.vert_range.max)
        bl = (self.horz_range.min, self.vert_range.min)

        coords = [br, tr, tl, bl]
        init_bounds = Bounds(*[Coord(*i) for i in coords])

        if not EXTENTS:
            return init_bounds

        return extend_bounds(init_bounds, EXTENTS)

    def create_perimeter_midpoints(self, EXTENTS=0):
        north = (self.horz_range.midpoint, self.vert_range.max + EXTENTS)
        south = (self.horz_range.midpoint, self.vert_range.min - EXTENTS)
        east = (self.horz_range.max + EXTENTS, self.vert_range.midpoint)
        west = (self.horz_range.min - EXTENTS, self.vert_range.midpoint)
        coords = [north, south, east, west]

        return PerimeterMidpoints(
            *[Coord(*i) for i in coords]
        )  # TODO potentially extract the extension here also

    # TODO should be in a seperate class devoted to graphing..
    def get_mpl_patch(self):
        return Rectangle(
            (self.horz_range.min, self.vert_range.min),
            self.horz_range.size,
            self.vert_range.size,
            fill=False,
            edgecolor="black",
            alpha=0.2,
        )


@dataclass
class MultiDomain:
    domains: list[Domain]

    @property
    def total_domain(self):
        min_x = min([i.horz_range.min for i in self.domains])
        max_x = max([i.horz_range.max for i in self.domains])
        min_y = min([i.vert_range.min for i in self.domains])
        max_y = max([i.vert_range.max for i in self.domains])
        return Domain(Range(min_x, max_x), Range(min_y, max_y))

    @property
    def external_coord_positions(self):
        return self.total_domain.create_perimeter_midpoints(EXTENTS=1)

    @property
    def extended_domain_with_external_coords(self):
        external_coords_domain = Domain.from_perimeter_mid_points(
            self.external_coord_positions
        )
        extended_bounds = external_coords_domain.create_bounds(EXTENTS=1)
        return Domain.from_bounds(extended_bounds)

    @property
    def extents(self):
        extended_domain = self.extended_domain_with_external_coords
        return (
            extended_domain.horz_range.as_tuple,
            extended_domain.vert_range.as_tuple,
        )
