from pathlib import Path
from typing import Optional
from geomeppy import IDF
from plan2eplus.constants import (
    SRC_PATH,
    PATH_TO_GRAPHBEM_OUTPUTS,
)
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import (
    add_rooms,
    add_all_output_requests,
)
from plan2eplus.helpers.ep_constants import OUTPUT_VARIABLE, RUNPERIOD, SITE
from plan2eplus.helpers.ep_helpers import (
    get_first_object,
)
from plan2eplus.helpers.output_requests import AdditionalVariablesFx
from plan2eplus.materials2.construction_set_map import (
    ConstructionSet,
    match_surface_to_constr_set,
)
from plan2eplus.visuals.interfaces import PlanZones
import polars as pl
import polars.selectors as cs
from rich import print as rprint
from plan2eplus.materials2.interfaces import Construction, get_default_material_dict
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.epw import EPW

# NOTES -> no AFN + some single sided ventilation...


input_path = (
    SRC_PATH / "graphbem"
)  # TODO separate repo with all things.. dont mix code and inputs

# windows..


def add_constructions_from_csv(idf: IDF):
    df = pl.read_csv(
        input_path / "My_Constructions.csv"
    )  # TODO separate repo with all things.. dont mix code and inputs

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


def assign_constructions(idf: IDF, constructions: list[Construction]):
    pz = PlanZones(idf)
    cset = ConstructionSet.from_list_of_constructions(constructions)
    for surface in pz.surfaces_and_subsurfaces:
        surface = match_surface_to_constr_set(surface, cset)
        surface.update_construction_on_idf()
    return idf


def create_graphbem_case(
    path_to_outputs: Path = PATH_TO_GRAPHBEM_OUTPUTS,
    epw: Optional[Path] = None,
    analysis_period: Optional[AnalysisPeriod] = None,
    get_additional_variables: AdditionalVariablesFx = None,
):
    case = EneryPlusCaseEditor(
        path_to_outputs, epw=epw, analysis_period=analysis_period
    )
    case.idf = add_rooms(case.idf, input_path)
    case.idf, constructions = add_constructions_from_csv(case.idf)
    case.idf = assign_constructions(case.idf, constructions)

    case.idf = add_all_output_requests(case.idf, get_additional_variables)

    case.compare_and_save()
    # case.run_idf(force_run=False)

    return case


if __name__ == "__main__":
    print("Running connectivity test..")
    case = create_graphbem_case()
    pz = PlanZones(case.idf)
