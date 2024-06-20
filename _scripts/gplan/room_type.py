# template for a single gplan floor plan, that consists of many plans 
from typing import TypedDict
from dataclasses import dataclass


@dataclass
class GPLANRoomAccess:
    path: str
    index : int


class GPLANRoomType(TypedDict):
    id: int
    label: str
    color: str
    left: int
    top: int 
    width: int 
    height: int