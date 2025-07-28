from typing import Optional, TypedDict, NamedTuple

from ..geometry.coords import Coord

from ..geometry.domain import Domain
from ..geometry.range import Range

from dataclasses import dataclass

GRAPH = "graph.json"
PLAN = "plan.json"
SUBSURFACES = "subsurfaces.json"


# TODO shared with svg2plan..
class WindowsJSON(TypedDict):
    id: int
    width: str
    height: str
    head_height: str
    opening_hieght: str
    model: str
    wtype: str


class DoorsJSON(TypedDict):
    id: int
    width: str
    height: str
    thickness: str
    material: str  # TODO


class SubSurfacesJSON(TypedDict):
    WINDOWS: list[WindowsJSON]
    DOORS: list[DoorsJSON]


class DetailsJSON(TypedDict):
    external: bool
    id: int


class GraphEdgeJSON(TypedDict):
    source: str
    target: str
    details: DetailsJSON


class RoomCoordinates(NamedTuple):
    id: int
    coords: Coord


@dataclass
class RoomFromJSON:
    id: int
    label: str
    left: str
    top: str
    width: str
    height: str
    color: Optional[str] = ""

    def convert_numbers(self):
        return [float(i) for i in [self.left, self.top, self.width, self.height]]

    def create_domain(self):
        left, top, width, height = self.convert_numbers()
        return Domain(Range(left, left + width), Range(top - height, top))

    # TODO remove from here..
    def create_zone_name(self):
        return f"0{self.id} `{self.label}`"  # TODO - make zero padded..

    # `{self.label}` -> # TODO to not break rest of code, going to break Plan Zones.. 5/31/25 8:17pm

    def get_coordinates(self):
        left, top, *_ = self.convert_numbers()
        return RoomCoordinates(self.id, Coord(left, top))


class WindowChangeData(NamedTuple):
    is_window_changed: bool = False
    value: float = 0
