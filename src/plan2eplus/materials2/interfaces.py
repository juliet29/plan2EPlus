from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import re
from geomeppy import IDF
from eppy.bunch_subclass import EpBunch

from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.constants import DUMMY_OUTPUT_PATH, MATERIALS_PATH
from rich import print as rprint
from typing import Literal, TypeVar

from plan2eplus.helpers.helpers import regex_match, regex_tester


# class RoughnessLevel(Enum):
#     MediumRough = 0

RoughnessLevel = Literal[
    "VeryRough", "Rough", "MediumRough", "MediumSmooth", "Smooth", "VerySmooth"
]


def test_material_regex():
    test1 = "WINDOWMATERIAL:GLAZING:EQUIVALENTLAYER"
    test2 = "MATERIAL:AIRGAP"
    test3 = "MATERIAL"
    test4 = "MATERIALPROPERTY:PHASECHANGEHYSTERESIS"  # anticase

    regex_tester(r"(MATERIAL:|\bMATERIAL\b)", test4)


@dataclass
class Material:
    name: str
    key: str
    ep_object: EpBunch
    # TODO all the possible things should be stored hear, possibly they have units as well.. ~ metric..

    def __repr__(self) -> str:
        return f"Material(name={self.name} key={self.key})"

    @classmethod
    def from_idf_object(cls, mat: EpBunch):
        return cls(mat.Name, mat.key, mat)

    def _add_to_idf(self, idf: IDF):
        # idf = deepcopy(_idf)
        # TODO protected -> only construction can call..
        idf.idfobjects[self.key.upper()].append(self.ep_object)
        return idf

    # can make assertions about the shape of the EpBunch OR wrap desired functions in class methods..


MaterialType = U = TypeVar("MaterialType", bound=Material)


@dataclass
class WallMaterial(Material):
    ...
    # for now since don't need the differentiation, can go super simple..

    # name: str
    # roughness: RoughnessLevel
    # # TODO can replace this with the epobject .. not doing anything special with these properties.., can add them as needed..
    # thickness: float
    # conductivity: float
    # density: float
    # specific_heat: float
    # thermal_absorptance: float = 0
    # solar_absorpatance: float = 0
    # visible_absorptance: float = 0

    # @classmethod
    # def from_idf_object(cls, mat:EpBunch):
    #     return WallMaterial(mat.Name, mat.Roughness, mat.Thickness, mat.Conductivity,mat.Density, mat.Specific_Heat) # type: ignore # TODO eplus error..
    # TODO also have epobject, in case want r-values, etc..


@dataclass
class AirGap(Material): ...


# NoMass
# WindowGas
# Air Gap
# Windo Glazing..


@dataclass
class Construction:
    name: str
    layers: list[Material]  # TODO fix -> should be generic material..

    @classmethod
    def from_str_list(
        cls, name: str, str_list: list[str], materials_dict: dict[str, MaterialType]
    ):
        layers = []
        for val in str_list:
            try:
                layers.append(materials_dict[val])
            except KeyError:
                raise Exception(
                    f"{val} is not in {sorted(list(materials_dict.keys()))}"
                )
        return cls(name, layers)

    def add_materials_to_idf(self, idf: IDF, material: Material):
        existing_material = idf.getobject(material.key.upper(), material.name)
        if not existing_material:
            idf = material._add_to_idf(idf=idf)

    def to_idf_object(self, _idf: IDF):
        """Object looks like => Name, Outside_Layer, Layer_2, Layer_2+1, ..., Layer_n"""

        idf = deepcopy(_idf)
        layer_names = [i.name for i in self.layers]
        other_keys = ["Outside_Layer"] + [
            f"Layer_{ix + 2}" for ix in range(len(self.layers) - 1)
        ]
        const_dict = {k: v for k, v in zip(other_keys, layer_names)}
        const_dict["Name"] = self.name

        idf.newidfobject("CONSTRUCTION", **const_dict)

        for mat in self.layers:
            self.add_materials_to_idf(idf, mat)

        return idf




class ConstructionSet:
    ...
    # responsible for assigning itself to different materials..


# TODO go to a different file
def find_material_keys(idf: IDF):
    material_keys = []
    pattern_str = r"(MATERIAL:|\bMATERIAL\b)"

    for key in idf.idfobjects.keys():
        if regex_match(pattern_str, key):  # TODO could prevent this repetition..
            material_keys.append(key)

    return material_keys
    # material_keys.append


def create_material_dict(idf: IDF) -> dict[str, Material]:
    all_materials = []
    material_keys = find_material_keys(idf)
    for key in material_keys:
        mats = idf.idfobjects[key]
        if mats:
            for mat in mats:
                all_materials.append(Material.from_idf_object(mat))

    mat_dict = {m.name: m for m in all_materials}
    return mat_dict


def get_default_material_dict():
    main_materials_idf = MATERIALS_PATH / "ASHRAE_2005_HOF_Materials.idf"
    case = EneryPlusCaseEditor(
        path_to_outputs=DUMMY_OUTPUT_PATH, starting_path=main_materials_idf
    )
    return create_material_dict(case.idf)


# TODO read in wall materials from IDF
# TODO create constructions and add to IDF

if __name__ == "__main__":
    print("\n---materials ---")
    main_materials_idf = MATERIALS_PATH / "ASHRAE_2005_HOF_Materials.idf"
    case = EneryPlusCaseEditor(
        path_to_outputs=DUMMY_OUTPUT_PATH, starting_path=main_materials_idf
    )
    mat_dict = create_material_dict(case.idf)

    MyExteriorWall = Construction.from_str_list(
        "My Exterior Wall",
        [
            "G01 16mm gypsum board",
            "F04 Wall air space resistance",
            "G01 16mm gypsum board",
        ],
        mat_dict,
    )
    new_idf = MyExteriorWall.to_idf_object(case.idf)
    # rprint(new_idf.idfobjects["CONSTRUCTION"])
    # rprint(new_idf.idfobjects["MATERIAL"])


    # case.idf.getobject("Material".upper(), "a fake material")


#
