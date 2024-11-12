from dataclasses import dataclass
from matplotlib.lines import Line2D
from typing import NamedTuple
from eppy.bunch_subclass import EpBunch

from helpers.geometry_interfaces import Coord
from helpers.geometry_interfaces import Range
from helpers.ep_helpers import PARTNER, get_original_subsurfaces, get_surface_by_name
from helpers.ep_geom_helpers import create_domain_for_rectangular_wall

from helpers.geometry_interfaces import Coordinate3D
def get_coords(surface):
    coords = [Coordinate3D(*i) for i in surface.coords]  # type:ignore
    assert len(coords) == 4
    xs = sorted(set([i.x for i in coords]))
    ys = sorted(set([i.y for i in coords]))
    zs = sorted(set([i.z for i in coords]))
    return xs, ys, zs

class SubsurfaceLocation(NamedTuple):
    axis: int
    location_in_other_axis: float

    @property
    def axis_name(self):
        d = {
            0: "x",
            1: "y",
            2: "z"
        }
        return d[self.axis]


@dataclass
class LineCoords:
    begin: Coord
    end: Coord

    def create_mpl_line(self, color="brown", linestyle="-", linewidth=2):
        return Line2D([self.begin.x, self.end.x], [self.begin.y, self.end.y], color=color, linestyle=linestyle, linewidth=linewidth)
    



def create_linecoords_for_subsurface(idf, subsurface: EpBunch):
    wall = get_surface_by_name(idf, subsurface.Building_Surface_Name)
    assert wall
    wall_dom = create_domain_for_rectangular_wall(wall)
    subsurface_start = wall_dom.width.min + float(subsurface.Starting_X_Coordinate)
    subsurface_end = subsurface_start + float(subsurface.Length)


    [res] = [SubsurfaceLocation(ix, i[0]) for ix, i in enumerate(get_coords(wall)) if len(i) == 1]

    if res.axis_name == "x":
        print(res,"x")
        a = Coord(res.location_in_other_axis, subsurface_start)
        b = Coord(res.location_in_other_axis, subsurface_end)
    elif res.axis_name == "y":
        a = Coord(subsurface_start, res.location_in_other_axis)
        b = Coord(subsurface_end, res.location_in_other_axis)
        print(res,"y")

    return LineCoords(a, b)




def plot_subsurfaces(idf, ax):
    subsurfaces = get_original_subsurfaces(idf)

    subsurface_colors = {
        "door": "saddlebrown",
        "window": "cornflowerblue"

    }

    for subsurface in subsurfaces:
        color = subsurface_colors["door"] if "door"in subsurface.Name.lower() else subsurface_colors["window"]
        l = create_linecoords_for_subsurface(idf, subsurface)
        ax.add_artist(l.create_mpl_line(color=color))

    return ax


