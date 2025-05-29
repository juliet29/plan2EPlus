from dataclasses import dataclass
from geomeppy import IDF
from matplotlib.lines import Line2D
from typing import Callable, NamedTuple
from eppy.bunch_subclass import EpBunch
from datetime import datetime
import polars as pl
from copy import deepcopy

from ...helpers.ep_geom_helpers import get_coords
from ...helpers.geometry_interfaces import Coord
from ...helpers.ep_helpers import get_original_subsurfaces, get_surface_by_name
from ...helpers.ep_geom_helpers import create_domain_for_rectangular_wall

from ...helpers.helpers import ContainsAsEqualsString
from ..setup.data_wrangle2 import create_dataframe_for_case
from ..setup.interfaces import CaseData
from ...helpers.variable_interfaces import all_variables as vars


class SubsurfaceLocation(NamedTuple):
    axis: int
    location_in_other_axis: float

    @property
    def axis_name(self):
        d = {0: "x", 1: "y", 2: "z"}
        return d[self.axis]


@dataclass
class LineCoords:
    begin: Coord
    end: Coord

    def create_mpl_line(self, color="brown", linestyle="-", linewidth=2):
        return Line2D(
            [self.begin.x, self.end.x],
            [self.begin.y, self.end.y],
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
        )


def create_linecoords(start_val: float, end_val: float, wall: EpBunch):
    [res] = [
        SubsurfaceLocation(ix, i[0])
        for ix, i in enumerate(get_coords(wall))
        if len(i) == 1
    ]

    a, b = None, None
    if res.axis_name == "x":
        a = Coord(res.location_in_other_axis, start_val)
        b = Coord(res.location_in_other_axis, end_val)
    elif res.axis_name == "y":
        a = Coord(start_val, res.location_in_other_axis)
        b = Coord(end_val, res.location_in_other_axis)

    if a and b:
        return LineCoords(a, b)
    else:
        raise Exception("could not retriev values to create line")


def create_linecoords_for_subsurface(idf, subsurface: EpBunch):
    wall = get_surface_by_name(idf, subsurface.Building_Surface_Name)
    assert wall
    wall_dom = create_domain_for_rectangular_wall(wall)
    subsurface_start = wall_dom.horz_range.min + float(subsurface.Starting_X_Coordinate)
    subsurface_end = subsurface_start + float(subsurface.Length)
    return create_linecoords(subsurface_start, subsurface_end, wall)


def get_airboundary_wall(name: str):  # TODO move to EpHelpers
    return " ".join(name.split(" ")[1:])  # TODO this may change if change AB logic..


def create_linecoords_for_airboundary(idf, construction_airboundary: EpBunch):
    wall = get_surface_by_name(idf, get_airboundary_wall(construction_airboundary.Name))
    assert wall
    wall_dom = create_domain_for_rectangular_wall(wall)
    return create_linecoords(wall_dom.horz_range.min, wall_dom.horz_range.max, wall)


### split here..


@dataclass
class SurfacePlotStyles:
    color: str
    linestyle: str
    fx: Callable[[IDF, EpBunch], LineCoords]


class SurfacePlotData(NamedTuple):
    surface: EpBunch
    style: SurfacePlotStyles


OPEN_LINESTYLE = "dashed"  # (0, (5, 1)) #"dashed"
CLOSED_LINESTYLE = "solid"


def get_surface_data_list(idf):
    surface_plot_styles = {
        "door": SurfacePlotStyles(
            "saddlebrown", CLOSED_LINESTYLE, create_linecoords_for_subsurface
        ),
        "window": SurfacePlotStyles(
            "cornflowerblue", CLOSED_LINESTYLE, create_linecoords_for_subsurface
        ),
        "airboundary": SurfacePlotStyles(
            "ghostwhite", OPEN_LINESTYLE, create_linecoords_for_airboundary
        ),
    }

    def get_style(surf):
        cstring = ContainsAsEqualsString(surf.Name.lower())
        match cstring:
            case "door":
                style = surface_plot_styles["door"]
            case "window":
                style = surface_plot_styles["window"]
            case "airboundary":
                style = surface_plot_styles["airboundary"]
            case _:
                raise Exception("Invalid surface type")
        assert style
        # TODO could return this for the open stateus fx
        return deepcopy(style)

    subsurfaces = get_original_subsurfaces(idf)
    airboundaries = idf.idfobjects["CONSTRUCTION:AIRBOUNDARY"]
    surfs_of_interest = subsurfaces + list(airboundaries)

    return [SurfacePlotData(surf, get_style(surf)) for surf in surfs_of_interest]


def get_opening_statuses(case: CaseData, time: datetime):
    df = create_dataframe_for_case(case, vars.afn.surface["opening_factor"])
    dff = (
        df.filter((pl.col("datetimes") == time))
        .filter(
            pl.col("space_names").str.contains("WINDOW")
            | pl.col("space_names").str.contains("DOOR")
        )
        .select(
            "space_names",
            "AFN Surface Venting Window or Door Opening Factor [fraction]",
        )
        .to_dict()
    )
    return {
        space: frac
        for space, frac in zip(
            dff["space_names"],
            dff["AFN Surface Venting Window or Door Opening Factor [fraction]"],
        )
    }


def update_styles_for_opening_status(
    case: CaseData, surf_data: list[SurfacePlotData], time: datetime
):
    def get_linestyle_for_status(name):
        val = statuses[name]
        return CLOSED_LINESTYLE if val == 0 else OPEN_LINESTYLE

    statuses = get_opening_statuses(case, time)
    for surf in surf_data:
        test_name = surf.surface.Name.upper()
        if "WINDOW" in test_name or "DOOR" in test_name:
            try:
                surf.style.linestyle = get_linestyle_for_status(test_name)
            except:
                surf.style.color = "slategrey"
                surf.style.linestyle = CLOSED_LINESTYLE
                print(f"{surf.surface.Name} NOT IN AFN.. ")

    return surf_data


def plot_surfaces(case: CaseData, time: datetime, ax):
    def plot_surf(surf_data: SurfacePlotData):
        surface, style = surf_data
        l = style.fx(case.idf, surface)
        ax.add_artist(l.create_mpl_line(color=style.color, linestyle=style.linestyle))

    surf_data_list = get_surface_data_list(case.idf)
    surf_data_list = update_styles_for_opening_status(case, surf_data_list, time)

    for surf_data in surf_data_list:
        plot_surf(surf_data)

    return ax, surf_data_list
