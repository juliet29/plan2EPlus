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

    def get_dict_for_plotting(self, color="blue", label=""):
        return dict(
        type="rect",
        xref="x",
        yref="y",
        fillcolor=color,
        x0=self.width.min,
        y0=self.height.min,
        x1=self.width.max,
        y1=self.height.max,
        label=dict(text=label),
    )



@dataclass
class Coord:
    x: float
    y: float

    def __getitem__(self, i):
        return (self.x, self.y)[i]


@dataclass
class Coordinate3D(Coord):
    z: float
