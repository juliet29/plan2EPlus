from typing import Optional
from matplotlib.axes import Axes
import numpy as np
from scipy.interpolate import CubicSpline
from plan2eplus.visuals.interfaces import PlanZones
from matplotlib import pyplot as plt
from rich import print as rprint


def plot_zone_domains(plan_zones: PlanZones, ax: Axes | None = None):
    if not ax:
        _, ax = plt.subplots()
    xlim, ylim = plan_zones.domains.extents
    ax.set(xlim=xlim, ylim=ylim)

    for d in plan_zones.domains.domains:
        ax.add_artist(d.get_mpl_patch())  # TODO - is this a property?

    for zone in plan_zones.zones:
        zone.plot_zone_name(ax)  # TODO should this be extracted?

    external_coords_patch = plan_zones.domains.external_coord_positions.get_mpl_patch()
    for patch in external_coords_patch:
        ax.add_artist(patch)

    # rprint("ext coord pos: ", plan_zones.domains.external_coord_positions.get_mpl_patch())

    plt.show()

    return ax


def create_spline(xs, ys):
    cs = CubicSpline(xs, ys)
    line_xs = np.linspace(start=xs[0], stop=xs[-1], num=20)
    return line_xs, cs(line_xs)


def plot_path_on_plot(coords: list[tuple[float, float]], ax: Optional[Axes] = None):
    print(f"==>> coords: {coords}")
    if not ax:
        _, ax = plt.subplots()
    xs = [i[0] for i in coords]
    print(f"==>> xs: {xs}")
    ys = [i[1] for i in coords]
    print(f"==>> ys: {ys}")
    line_xs, line_ys = create_spline(xs, ys)
    ax.plot(line_xs, line_ys)
    return ax
