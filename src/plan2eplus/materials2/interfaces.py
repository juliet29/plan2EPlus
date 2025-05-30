from dataclasses import dataclass
from enum import Enum


class RoughnessLevel(Enum):
    MediumRough = 0


@dataclass
class Material: ...


@dataclass
class WallMaterial(Material):
    name: str
    roughness: str
    thickness: float
    conductivity: float
    density: float
    specific_heat: float


@dataclass
class Construction:
    name: str
    layers: list[Material]

    def to_idf_object(self):
        pass


# TODO read in wall materials from IDF
# TODO create constructions and add to IDF 