
# TODO shared with svg2plan.. 
from typing import Optional, TypedDict, NamedTuple


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


class RoomTypeJSON(TypedDict):
    id: int
    label: str
    left: str
    top: str
    width: str
    height: str
    color: Optional[str]



class DetailsJSON(TypedDict):
    external: bool
    id: int

class GraphEdgeJSON(TypedDict):
    source: str
    target: str
    details: DetailsJSON