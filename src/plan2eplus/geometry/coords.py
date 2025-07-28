from matplotlib.text import Text
from plan2eplus.helpers.helpers import dataclass_as_dict
from plan2eplus.geometry.directions import WallNormalNames


from dataclasses import dataclass


# TODO organize classes -> dunder methods, then class methods, then properties, then other things..


@dataclass(frozen=True)
class Coord:
    x: float
    y: float

    def __getitem__(self, i):
        return (self.x, self.y)[i]

    @property
    def pair(self):
        return (self.x, self.y)


@dataclass
class CoordList:
    # sample_coords: int = 0

    @property
    def asdict(self) -> dict[str, Coord]:
        return dataclass_as_dict(self)

    @property
    def as_pairs_dict(self):  # TOOD use a dict here..
        return {k: v.pair for k, v in self.asdict.items()}

    @property
    def as_pairs(self):  # TOOD use a dict here..
        return [v.pair for v in self.asdict.values()]


@dataclass
class PerimeterMidpoints(CoordList): #NOTE: never create dependency on directions! 
    NORTH: Coord
    SOUTH: Coord
    EAST: Coord
    WEST: Coord

    def __getitem__(self, i):  # :Literal["NORTH", "SOUTH", "EAST", "WEST" ] WallNormalNames
        return self.asdict[i]

    @property
    def keys(self): # -> WallNormalNames:
        return list(self.asdict.keys()) # type: ignore

    def get_mpl_patch(self):
        def create_text_patch(x, y, text):
            shown_text = f"{text}\n({x}, {y})"
            return Text(x, y, shown_text)  # TODO can customize..

        # for i in self.keys:
        #     rprint(i, self[i].pair)
        text_patches = [create_text_patch(*self[i].pair, i) for i in self.keys]
        return text_patches


@dataclass
class Bounds(CoordList):
    br: Coord
    tr: Coord
    tl: Coord
    bl: Coord


@dataclass(frozen=True)
class Coordinate3D(Coord):
    z: float

    def get_pair(self, l1, l2):
        return Coord(self.__dict__[l1], self.__dict__[l2])
