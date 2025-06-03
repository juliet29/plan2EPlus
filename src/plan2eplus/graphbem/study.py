from geomeppy import IDF
from plan2eplus.constants import SRC_PATH, GRAPHBEM_PATH
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import add_rooms, finish_creating_ezcase,    add_all_output_requests
from plan2eplus.materials2.construction_set_map import ConstructionSet, match_surface_to_constr_set
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


def add_constructions_from_csv(idf: IDF):
    df = pl.read_csv(input_path / "My_Constructions.csv")
    layer_cols = df.select(cs.contains("Layer")).columns


    constructions = []
    for row in df.iter_rows(named=True):
        material_list = [v for k, v in row.items() if k in layer_cols and v]
        name = row["Name"]
        c = Construction.from_list_of_material_names(
            name, material_list, get_default_material_dict()
        )
        idf = c.add_construction_to_idf(idf)
        constructions.append(c)

    return idf, constructions

    # for construction in constructions:
    #     construction.to_idf


def assign_constructions(idf: IDF, constructions:list[Construction]):
    pz = PlanZones(idf)
    cset = ConstructionSet.from_list_of_constructions(constructions)
    sub = pz.surfaces_and_subsurfaces
    rprint(f"id in assign {id(sub)}")
    for surface in pz.surfaces_and_subsurfaces:
        surface = match_surface_to_constr_set(surface, cset)
        surface.update_construction_on_idf()

    
    # pz.update_constructions_for_all_surfaces()
    # idf.printidf()
    rprint(pz.surfaces_and_subsurfaces[0].ep_object)
    return idf


def test_graph_bem():
    case = EneryPlusCaseEditor(GRAPHBEM_PATH)
    case.idf = add_rooms(case.idf, input_path)
    case.idf, constructions = add_constructions_from_csv(case.idf)
    case.idf = assign_constructions(case.idf, constructions)
    case.idf = add_all_output_requests(case.idf)
    case.compare_and_save()
    case.run_idf(force_run=True)
    return case.idf
    # idf.printidf()
    
    

    # print(case.idf.getsubsurfaces())

    # rprint(case.idf.idfobjects["CONSTRUCTION"])
    # rprint(case.idf.idfobjects["MATERIAL"])
    # pz = PlanZones(case.idf)
    # pz.plot_zone_domains()
    
    # pz.zones[0].get_plan_name(input_path)

    # read construction as df
    # extract name, put layers into list


if __name__ == "__main__":
    print("Running connectivity test..")
    idf = test_graph_bem()
    pz = PlanZones(idf)
    # pz.plot_zone_domains()
    # zone = pz.get_zone_by_num(0)
    # for wall in zone.walls:
    #     partner_wall = wall.partner_wall(idf)
    #     rprint([wall, wall.idf_name, "|", partner_wall])

