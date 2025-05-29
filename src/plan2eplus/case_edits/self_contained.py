from plan2eplus.constants import IDD_PATH, IDF_PATH
from plan2eplus.case_edits.extended_idf import ExtendedIDF
from plan2eplus.helpers.ep_geom_helpers import WallNormal
from plan2eplus.plan.local_room_def import RoomDefinition, create_two_room_layout
from plan2eplus.plan.plan_to_eppy import add_eppy_blocks
from plan2eplus.subsurfaces.creator import add_subsurfaces_to_case
from plan2eplus.subsurfaces.interfaces import (
    SubsurfaceAttributes,
    SubsurfacePair,
    SubsurfaceObjects,
    NinePointsLocator,
)
from plan2eplus.helpers.geometry_interfaces import Dimensions


def test_ezcase():
    ExtendedIDF.setiddname(IDD_PATH)
    idf1 = ExtendedIDF(IDF_PATH)

    plan = create_two_room_layout(RoomDefinition(5, 5), RoomDefinition(10, 5))
    idf1 = add_eppy_blocks(idf1, plan)
    ss1 = SubsurfacePair(
        0,
        1,
        SubsurfaceAttributes(
            SubsurfaceObjects.DOOR,
            None,
            Dimensions(1, 2),
            NinePointsLocator.bottom_middle,
        ),
    )
    ss2 = SubsurfacePair(
        0,
        WallNormal.NORTH,
        SubsurfaceAttributes(
            SubsurfaceObjects.WINDOW,
            None,
            Dimensions(1, 2),
            NinePointsLocator.middle_middle,
        ),
    )
    return idf1
    idf1 = add_subsurfaces_to_case(idf1, [ss1, ss2])
