from ...helpers.ep_helpers import WallNormal
from copy import deepcopy
from ...helpers.geometry_interfaces import Domain, Range

NodePositions = dict[str, tuple[float, float]]


def get_bounds_of_positioned_graph(pos: NodePositions):
    x_values = [coord[0] for coord in pos.values()]
    y_values = [coord[1] for coord in pos.values()]

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    return Domain(Range(x_min, x_max), Range(y_min, y_max))


def create_cardinal_positions(_positions: NodePositions, PAD=1.4):
    positions = deepcopy(_positions)
    c = get_bounds_of_positioned_graph(positions)
    mid_x = c.horz_range.midpoint
    mid_y = c.vert_range.midpoint

    res = [
        (mid_x, c.vert_range.max + PAD),
        (mid_x, c.vert_range.min - PAD),
        (c.horz_range.min - PAD, mid_y),
        (c.horz_range.max + PAD, mid_y),
    ]

    drns = [WallNormal.NORTH, WallNormal.SOUTH, WallNormal.WEST, WallNormal.EAST]
    temp = {i.name: r for i, r in zip(drns, res)}

    positions.update(temp)
    return positions
