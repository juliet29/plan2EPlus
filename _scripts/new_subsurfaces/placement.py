from typing import Callable, NamedTuple
from new_subsurfaces.interfaces import Dimensions
from new_subsurfaces.geometry_interfaces import (
    Coord,
    Domain,
)


class PlacementPoint(NamedTuple):
    point: Coord
    functions: list[Callable[[Coord, Dimensions], Coord]]


def push_down(init_pt: Coord, dim: Dimensions):
    return Coord(init_pt.x, init_pt.y - dim.height)


def push_left(init_pt: Coord, dim: Dimensions):
    return Coord(init_pt.x - dim.width, init_pt.y)


def push_down_half(init_pt: Coord, dim: Dimensions):
    return Coord(init_pt.x, init_pt.y - dim.height / 2)


def push_left_half(init_pt: Coord, dim: Dimensions):
    return Coord(init_pt.x - dim.width / 2, init_pt.y)


def create_nine_points_for_domain(d: Domain, buffer=0.01):
    w_min = d.width.buffered_min(buffer)
    w_mid = d.width.midpoint()
    w_max = d.width.buffered_max(buffer)
    h_min = d.height.buffered_min(buffer)
    h_mid = d.height.midpoint()
    h_max = d.height.buffered_max(buffer)

    nine_points = {
        "top_left": PlacementPoint(
            Coord(w_min, h_max),
            [
                push_down,
            ],
        ),
        "top_middle": PlacementPoint(Coord(w_mid, h_max), [push_down, push_left_half]),
        "top_right": PlacementPoint(Coord(w_max, h_max), [push_down, push_left]),
        "middle_left": PlacementPoint(
            Coord(w_min, h_mid),
            [
                push_down_half,
            ],
        ),
        "middle_middle": PlacementPoint(
            Coord(w_mid, h_mid), [push_down_half, push_left_half]
        ),
        "middle_right": PlacementPoint(
            Coord(w_max, h_mid), [push_down_half, push_left]
        ),
        "bottom_left": PlacementPoint(Coord(w_min, h_min), []),
        "bottom_middle": PlacementPoint(Coord(w_mid, h_min), [push_left_half]),
        "bottom_right": PlacementPoint(Coord(w_max, h_min), [push_left]),
    }

    return nine_points
