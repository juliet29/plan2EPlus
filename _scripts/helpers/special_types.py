from geometry.wall_normal import WallNormal
from typing import List, Tuple, Union
from plan.room_class import GPLANRoomType, GPLANRoomAccess

ZonePairTuple = Tuple[int, int]
ZoneDirectionTuple = Tuple[int, WallNormal]
PairType = Union[ZoneDirectionTuple, ZonePairTuple]


GeometryType = Union[List[GPLANRoomType], GPLANRoomAccess]
