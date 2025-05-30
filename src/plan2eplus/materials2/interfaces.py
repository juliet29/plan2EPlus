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

RoughnessLevel = Literal['VeryRough', 'Rough', 'MediumRough', 'MediumSmooth', 'Smooth', 'VerySmooth']

@dataclass
class Material:
    name: str
    key: str
    ep_object: EpBunch
    # TODO all the possible things should be stored hear, possibly they have units as well.. ~ metric.. 

    def __repr__(self) -> str:
        return f"Material(name={self.name} key={self.key})"

    @classmethod
    def from_idf_object(cls, mat:EpBunch):
        return cls(mat.Name, mat.key, mat)
        
MaterialType = U = TypeVar('MaterialType', bound=Material)


@dataclass
class WallMaterial(Material):
    ...
    # for now since don't need the differentiation, can go super simple.. 

@dataclass
class AirGap(Material):
    ...
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

# NoMass
# WindowGas
# Air Gap 
# Windo Glazing.. 

@dataclass
class Construction:
    name: str
    layers: list[type[Material]] # TODO fix -> should be generic material.. 

    @classmethod
    def from_str_list(cls, name:str, str_list:list[str], materials_dict:dict[str, MaterialType]):
        layers = []
        for val in str_list:
            try:
                layers.append(materials_dict[val])
            except:
                raise Exception(f"{val} is not in {materials_dict.keys()}")
        return cls(name, layers)

    def to_idf_object(self):
        pass


def find_material_keys(idf:IDF):
    material_keys = []

    pattern_str = r"(MATERIAL:|\bMATERIAL\b)"

    for key in idf.idfobjects.keys():
        if regex_match(pattern_str, key): # TODO could prevent this repetition.. 
            material_keys.append(key)

    return material_keys
        # material_keys.append

def create_material_dict(idf:IDF):
    all_materials = []
    material_keys = find_material_keys(idf)
    for key in material_keys:
        mats = idf.idfobjects[key]
        if mats:
            for mat in mats:
                all_materials.append(Material.from_idf_object(mat))
    
    mat_dict = {m.name : m for m in all_materials}
    return mat_dict


# TODO read in wall materials from IDF
# TODO create constructions and add to IDF 

if __name__ == "__main__":
    print("\n---materials ---")
    main_materials_idf = MATERIALS_PATH / "ASHRAE_2005_HOF_Materials.idf"
    case = EneryPlusCaseEditor(
        path_to_outputs=DUMMY_OUTPUT_PATH, starting_path=main_materials_idf
    )
    mat_dict = create_material_dict(case.idf)
    rprint(mat_dict.keys())
    # mats = case.idf.idfobjects["Material".upper()]
    # # rprint(case.idf.idfobjects.keys())

    # test1 = 'WINDOWMATERIAL:GLAZING:EQUIVALENTLAYER'
    # test2 = 'MATERIAL:AIRGAP'
    # test3 = "MATERIAL"
    # test4 = "MATERIALPROPERTY:PHASECHANGEHYSTERESIS" # anticase

    # regex_tester(r"(MATERIAL:|\bMATERIAL\b)", test4)
    # # rprint(mats[0].__dict__)
    # rprint(mats[0].key)
    # rprint(WallMaterial.from_idf_object(mats[0]))
    # # mats[0]


    # materials = [WallMaterial.from_idf_object(i) for i in mats]
    # md = {i.name : i for i in materials}
    # rprint(md)
    # have to do for air 

    # MyExteriorWall = Construction.from_str_list("My Exterior Wall", ["G01 16mm gypsum board",  "G01 16mm gypsum board" ], md)
    # rprint(MyExteriorWall)
    # TODO read from csv... 
    # TODO must add airgaps also.. 

    
    # mat = case.idf.getobject("Material", "F06 EIFS finish")
    # rprint(mat)


# 
def test_material_regex():
    test1 = 'WINDOWMATERIAL:GLAZING:EQUIVALENTLAYER'
    test2 = 'MATERIAL:AIRGAP'
    test3 = "MATERIAL"
    test4 = "MATERIALPROPERTY:PHASECHANGEHYSTERESIS" # anticase
    
    regex_tester(r"(MATERIAL:|\bMATERIAL\b)", test4)