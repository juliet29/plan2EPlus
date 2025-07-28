from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import re
from geomeppy import IDF
from eppy.bunch_subclass import EpBunch

from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.paths import PATH_TO_DUMMY_OUTPUTS, MATERIALS_PATH
from rich import print as rprint
from typing import Literal, TypeVar

from plan2eplus.helpers.helpers import regex_match, regex_tester


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


ConstructionTypes = Literal[
    "exterior", "interior", "roof", "cieling", "floor", "door", "window"
]


@dataclass
class Construction:
    name: str
    layers: list[Material]
    construction_type: ConstructionTypes | None = None

    @classmethod
    def from_list_of_material_names(
        cls, name: str, str_list: list[str], materials_dict: dict[str, Material]
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

    def add_material_to_idf(self, idf: IDF, material: Material):
        existing_material = idf.getobject(material.key.upper(), material.name)
        if not existing_material:
            idf = material._add_to_idf(idf=idf)

    def add_construction_to_idf(self, _idf: IDF):
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
            self.add_material_to_idf(idf, mat)

        return idf

    def assign_default_mapping(self, construction_type: ConstructionTypes):
        self.construction_type = construction_type

    # responsible for assigning itself to different materials..


# TODO move to a different file
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
        path_to_outputs=PATH_TO_DUMMY_OUTPUTS, starting_path=main_materials_idf
    )
    return create_material_dict(case.idf)


def create_test_constructions():
    mat_dict = get_default_material_dict()
    const_a = Construction.from_list_of_material_names(
        "My Exterior Wall",
        [
            "G01 16mm gypsum board",
            "F04 Wall air space resistance",
            "G01 16mm gypsum board",
        ],
        mat_dict,
    )

    const_b = Construction.from_list_of_material_names(
        "My Floor",
        [
            "G01 16mm gypsum board",
            "F04 Wall air space resistance",
            "G01 16mm gypsum board",
        ],
        mat_dict,
    )

    const_c = Construction.from_list_of_material_names(
        "My Roof",
        [
            "G01 16mm gypsum board",
            "F04 Wall air space resistance",
            "G01 16mm gypsum board",
        ],
        mat_dict,
    )
    return const_a, const_b, const_c


# TODO read in wall materials from IDF
# TODO create constructions and add to IDF

if __name__ == "__main__":
    print("\n---materials ---")
    main_materials_idf = MATERIALS_PATH / "ASHRAE_2005_HOF_Materials.idf"
    case = EneryPlusCaseEditor(
        path_to_outputs=PATH_TO_DUMMY_OUTPUTS, starting_path=main_materials_idf
    )
    mat_dict = create_material_dict(case.idf)

    MyExteriorWall = Construction.from_list_of_material_names(
        "My Exterior Wall",
        [
            "G01 16mm gypsum board",
            "F04 Wall air space resistance",
            "G01 16mm gypsum board",
        ],
        mat_dict,
    )
    new_idf = MyExteriorWall.add_construction_to_idf(case.idf)
    # rprint(new_idf.idfobjects["CONSTRUCTION"])
    # rprint(new_idf.idfobjects["MATERIAL"])

    # case.idf.getobject("Material".upper(), "a fake material")


#
