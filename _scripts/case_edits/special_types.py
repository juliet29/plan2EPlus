from geometry.wall import WallNormal
from typing import List, Tuple, Union
from gplan.room_class import GPLANRoomType, GPLANRoomAccess

ZonePairTuple = Tuple[int, int]
ZoneDirectionTuple = Tuple[int, WallNormal]
PairType = Union[ZoneDirectionTuple, ZonePairTuple] 


GeometryType = Union[List[GPLANRoomType], GPLANRoomAccess]