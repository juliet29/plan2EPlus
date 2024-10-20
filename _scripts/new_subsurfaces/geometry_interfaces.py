from dataclasses import dataclass


class InvalidRangeException(Exception):
    def __init__(self, min, max) -> None:
        super().__init__(self)
        print(f"{min:.2f} cannot be less than {max:.2f}")


@dataclass(frozen=True)
class Range:
    min: float
    max: float

    def __post_init__(self):
        try:
            assert self.min <= self.max
        except AssertionError:
            raise InvalidRangeException(self.min, self.max)

    @property
    def size(self):
        return self.max - self.min

    def buffered_min(self, val):
        return self.min + val * self.size

    def buffered_max(self, val):
        return self.max - val * self.size

    def midpoint(self):
        return (self.min + self.max) / 2


@dataclass(frozen=True)
class Domain:
    width: Range
    height: Range


@dataclass
class Coord:
    x: float
    y: float

    def __getitem__(self, i):
        return getattr(self, i)


@dataclass
class Coordinate3D(Coord):
    z: float
