from pathlib import Path
from geomeppy import IDF, extractor
import re

from constructions.materials import get_construction_set_materials

def find_desired_window_constructions(idf: IDF):
    pattern = re.compile("Sgl Clr \dmm")
    return [i for i in idf.idfobjects["CONSTRUCTION"] if pattern.match(i.Name)]


def edit_window_names(idf: IDF):
    wcons = find_desired_window_constructions(idf)
    assert len(wcons) == 2
    idf.copyidfobject(wcons[0])
    wcons = find_desired_window_constructions(idf)
    assert len(wcons) == 3
    new_names = [f"{t} Window {i.Name}" for t,i in zip(["Light", "Medium", "Heavy"] ,wcons)]
    for i, n in zip(wcons, new_names):
        i.Name = n
    return idf

def create_unified_constructions_idf():
    path_to_constructions = Path.cwd() / "cases" / "constructions"
    cidf = IDF(path_to_constructions / "ASHRAE_2005_HOF_Materials.idf")
    new_idf_path = path_to_constructions / "CombinedConstructs.idf"
    with new_idf_path.open("w"):
        pass  
    new_idf = IDF(new_idf_path)
    extractor.copy_constructions(cidf, new_idf)

    win_cons_idf = IDF(path_to_constructions / "WindowConstructs.idf")
    win_glass_mat_idf = IDF(path_to_constructions / "WindowGlassMaterials.idf")
    augmented_win_cons_idf = extractor.copy_constructions(win_glass_mat_idf, win_cons_idf)


    wcons = find_desired_window_constructions(augmented_win_cons_idf)
    wmats = get_construction_set_materials(wcons)

    res = wcons + wmats
    for i in res:
        new_idf.copyidfobject(i)

    new_idf = edit_window_names(new_idf)

    new_idf.save()

    return new_idf

