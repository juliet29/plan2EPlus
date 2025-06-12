import pytest
from plan2eplus.helpers.geometry_interfaces import (
    Domain,
    Range,
    PerimeterMidpoints,
    Coord,
    Bounds,
    MultiDomain
)
from rich import print as rprint

# TODO rename "test geometry interfaces"

# TODO test that getting the external domain from a list of domains is accurate..

@pytest.fixture
def sample_coords():
    return [(0, 0), (1, 0), (1, 1), (0, 1)]


@pytest.fixture
def simple_domain():
    return Domain(horz_range=Range(0, 2), vert_range=Range(0, 2))



def test_bounds_as_pairs(sample_coords:list[tuple]):
    bounds = Bounds(*[Coord(*i) for i in sample_coords])
    assert len(bounds.as_pairs) == 4

def test_create_perimeter_midpoints():
    pm = PerimeterMidpoints(north=Coord(0,0), south=Coord(0,0), east=Coord(0,0),west=Coord(0,0))
    assert pm 


def test_find_external_coords(simple_domain: Domain):
    external_coords = simple_domain.create_perimeter_midpoints(EXTENTS=1)
    expected_coords = PerimeterMidpoints(
        north=Coord(1, 3), south=Coord(1, -1), east=Coord(3, 1), west=Coord(-1, 1)
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
    domain_a = Domain(Range(0,1), Range(0,1))
    domain_b = Domain(Range(1,2), Range(0,1))
    expected_total_doman = Domain(Range(0,2), Range(0,1))
    md = MultiDomain([domain_a, domain_b])
    assert md.total_domain == expected_total_doman


def test_finding_extended_domain(simple_domain: Domain):
    extended_domain = MultiDomain([simple_domain]).extended_domain_with_external_coords
    expected_domain = Domain(horz_range=Range(-2, 4), vert_range=Range(-2, 4))
    assert extended_domain == expected_domain











if __name__ == "__main__":
    pass
    # test_domain = Domain(horz_range=Range(0, 2), vert_range=Range(0, 2))
    # PerimeterMidpoints(north=Coord(0,0), south=Coord(0,0), east=Coord(0,0),west=Coord(0,0))
    # pm = test_domain.create_perimeter_midpoints(EXTENTS=1)
    # rprint(pm)



