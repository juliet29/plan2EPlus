from eppy.bunch_subclass import EpBunch
from geomeppy import IDF
from helpers.ep_geom_helpers import (
    create_domain_for_rectangular_wall,
    create_domain_for_subsurface,
)
from helpers.ep_helpers import get_surface_of_subsurface
from helpers.plots import plot_one_shape

COLOR_1 = "rgba(26,150,65,0.5)"
COLOR_2 = "rgba(26,90,65,0.5)"


def plot_subsurface_and_surface(idf: IDF, subsurface: EpBunch):
    surface = get_surface_of_subsurface(idf, subsurface)
    assert surface
    surface_dict = create_domain_for_rectangular_wall(surface).get_dict_for_plotting(
        COLOR_1
    )
    subsuface_dict = create_domain_for_subsurface(subsurface).get_dict_for_plotting(
        COLOR_2
    )

    fig = plot_one_shape(surface_dict)
    fig = plot_one_shape(subsuface_dict, fig=fig)
    return fig
