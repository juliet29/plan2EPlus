from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import pytest
from plan2eplus.connectivity_study.study import create_connectivity_case
from plan2eplus.helpers.geometry_interfaces import (
    Domain,
    Range,
    PerimeterMidpoints,
    Coord,
    Bounds,
    MultiDomain,
)
from rich import print as rprint

from plan2eplus.visuals.graph_plot import find_points_along_path, plot_path_on_plot

# TODO rename "test geometry interfaces"

# TODO test that getting the external domain from a list of domains is accurate..


@pytest.fixture
def sample_coords():
    return [(0, 0), (1, 0), (1, 1), (0, 1)]


@pytest.fixture
def simple_domain():
    return Domain(horz_range=Range(0, 2), vert_range=Range(0, 2))


def test_bounds_as_pairs(sample_coords: list[tuple]):
    bounds = Bounds(*[Coord(*i) for i in sample_coords])
    assert len(bounds.as_pairs) == 4


def test_create_perimeter_midpoints():
    pm = PerimeterMidpoints(
        NORTH=Coord(0, 0), SOUTH=Coord(0, 0), EAST=Coord(0, 0), WEST=Coord(0, 0)
    )
    assert pm


def test_find_external_coords(simple_domain: Domain):
    external_coords = simple_domain.create_perimeter_midpoints(EXTENTS=1)
    expected_coords = PerimeterMidpoints(
        NORTH=Coord(1, 3), SOUTH=Coord(1, -1), EAST=Coord(3, 1), WEST=Coord(-1, 1)
    )
    assert external_coords == expected_coords


# @pytest.mark.skip()
def test_find_domain_extents_from_external_coords(simple_domain: Domain):
    external_coords = simple_domain.create_perimeter_midpoints(EXTENTS=1)
    external_coords_domain = Domain.from_perimeter_mid_points(external_coords)
    extended_bounds = external_coords_domain.create_bounds(EXTENTS=1)

    extended_domain = Domain.from_bounds(extended_bounds)
    expected_domain = Domain(horz_range=Range(-2, 4), vert_range=Range(-2, 4))
    assert extended_domain == expected_domain


def test_finding_total_domain():
    domain_a = Domain(Range(0, 1), Range(0, 1))
    domain_b = Domain(Range(1, 2), Range(0, 1))
    expected_total_doman = Domain(Range(0, 2), Range(0, 1))
    md = MultiDomain([domain_a, domain_b])
    assert md.total_domain == expected_total_doman


def test_finding_extended_domain(simple_domain: Domain):
    extended_domain = MultiDomain([simple_domain]).extended_domain_with_external_coords
    expected_domain = Domain(horz_range=Range(-2, 4), vert_range=Range(-2, 4))
    assert extended_domain == expected_domain


# TODO clean this up, dont want to have to maintain all these tests.. 

@pytest.fixture
def connectivity_idf():
    return create_connectivity_case()

@pytest.fixture
def expected_coords():
    return  [
        Coord(x=0.0, y=2.0),
        Coord(x=1.0, y=1.5),
        Coord(x=2.0, y=1.5),
        Coord(x=3.0, y=1.5),
        Coord(x=4.0, y=2.0),
    ]

def test_find_points_along_path(connectivity_idf, expected_coords): 
    path = ["WEST", "b", "a", "EAST"]
    coords = find_points_along_path(connectivity_idf, path)
    assert coords == expected_coords




def test_plot_path(expected_coords):
    coords = [i.pair for i in expected_coords]
    ax:Axes = plot_path_on_plot(coords)
    result = ax.get_lines()[0]
    assert isinstance(result, Line2D)
    xdata = result.get_xdata()
    print(f"==>> xdata: {xdata}")
    ydata = result.get_ydata()
    xs = [i[0] for i in coords]
    ys = [i[1] for i in coords]
    # TODO check intersection, they will not be equal.. 
    assert xdata
    assert ydata

    # TODO test that works both ways... x and y.. 




if __name__ == "__main__":
    pass
    # test_domain = Domain(horz_range=Range(0, 2), vert_range=Range(0, 2))
    # PerimeterMidpoints(north=Coord(0,0), south=Coord(0,0), east=Coord(0,0),west=Coord(0,0))
    # pm = test_domain.create_perimeter_midpoints(EXTENTS=1)
    # rprint(pm)
