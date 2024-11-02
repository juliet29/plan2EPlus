from pathlib import Path
from typing import Literal
from eppy.bunch_subclass import EpBunch
from eppy.constructions import thermal_properties
from geomeppy import IDF
from constructions.materials import get_construction_set_materials
from constructions.organize import assign_material_to_surface, organize_cons_set

CONSTRUCTION_SET_TYPE = Literal["Light", "Medium", "Heavy"]


def get_constructions_idf():
    path_to_constructions = Path.cwd() / "cases" / "constructions"
    return IDF(path_to_constructions / "CombinedConstructs.idf")


def get_cons_set_by_type(cons_set_type: CONSTRUCTION_SET_TYPE) -> list[EpBunch]:
    cidf = get_constructions_idf()
    cons = cidf.idfobjects["CONSTRUCTION"]
    return [i for i in cons if cons_set_type in i.Name]


def add_cons_set_to_idf(idf: IDF, cons_set_type: CONSTRUCTION_SET_TYPE):
    cons_set = get_cons_set_by_type(cons_set_type)
    mats = get_construction_set_materials(cons_set)
    res = cons_set + mats
    for i in res:
        idf.copyidfobject(i)  # type: ignore
    # TODO only do it once!
    return idf


def assign_cons_set(idf: IDF, cons_set_type: CONSTRUCTION_SET_TYPE):
    cons_set = get_cons_set_by_type(cons_set_type)
    idf = add_cons_set_to_idf(idf, cons_set_type)
    cad = organize_cons_set(cons_set)

    surfaces = idf.getsurfaces()
    subsurfaces = idf.getsubsurfaces()
    res = surfaces + subsurfaces
    for surface in res:
        assign_material_to_surface(surface, cad)
    return idf


def study_r_values(cons_set: list[EpBunch]):
    return [(i.Name, thermal_properties.rvalue(i)) for i in cons_set]
