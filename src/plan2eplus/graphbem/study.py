from geomeppy import IDF
from plan2eplus.constants import SRC_PATH, DUMMY_OUTPUT_PATH
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import add_rooms, finish_creating_ezcase
from plan2eplus.visuals.interfaces import PlanZones
import polars as pl
import polars.selectors as cs
from rich import print as rprint
from plan2eplus.materials2.interfaces import Construction, get_default_material_dict

# from plan2eplus.subsurfaces.interfaces import (
#     NinePointsLocator,
#     SubsurfaceAttributes,
#     SubsurfaceObjects,
#     SubsurfacePair,
# )


# NOTES -> no AFN + some single sided ventilation... 


input_path = SRC_PATH / "graphbem"

# windows.. 

def add_materials(idf: IDF):
    df = pl.read_csv(input_path / "My_Constructions.csv")
    layer_cols = df.select(cs.contains("Layer")).columns
    
    # constructions:list = []
    for row in df.iter_rows(named=True):
        material_list = [v for k,v in row.items() if k in layer_cols and v]
        name = row["Name"]
        c = Construction.from_str_list(name, material_list, get_default_material_dict())
        idf = c.to_idf_object(idf)

    return idf

    # for construction in constructions:
    #     construction.to_idf

def assign_materials():
    pass



def test_graph_bem():
    case = EneryPlusCaseEditor(DUMMY_OUTPUT_PATH)
    case.idf = add_rooms(case.idf, input_path)
    case.idf = add_materials(case.idf)
    rprint(case.idf.idfobjects["CONSTRUCTION"])
    rprint(case.idf.idfobjects["MATERIAL"])
    # pz = PlanZones(case.idf)
    # pz.plot_zone_domains()
    # case.idf.printidf()
    # pz.zones[0].get_plan_name(input_path)

    # read construction as df
    # extract name, put layers into list 



        





if __name__ == "__main__":
    print("Running connectivity test..")
    test_graph_bem()
