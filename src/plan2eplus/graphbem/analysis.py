from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.graphbem.study import test_graph_bem
from plan2eplus.helpers.helpers import chain_flatten
from plan2eplus.helpers.read_sql import get_collection_for_variable, get_sql_results
from plan2eplus.studies.setup.data_wrangle import (
    create_init_data,
    create_dataframe_for_case,
)
from plan2eplus.constants import DUMMY_OUTPUT_PATH, GRAPHBEM_PATH
from rich import print as rprint
import altair as alt

from plan2eplus.visuals.interfaces import PlanZones
from plan2eplus.visuals.idf_name import decompose_idf_name
import polars as pl

CASE_NAME = "graphbem"
alt.renderers.enable("browser")

variables = {
    "TEMP": "Zone Mean Air Temperature",
    "SURF_OUT_TEMP": "Surface Outside Face Temperature",
    "SURF_IN_TEMP": "Surface Inside Face Temperature",
}


def analyze_zones():
    sql_result = get_sql_results(GRAPHBEM_PATH)
    df = create_dataframe_for_case(CASE_NAME, sql_result, variables["TEMP"])
    rprint(df.head())
    base = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="datetimes",
            y=alt.Y("values", title=variables["TEMP"]).scale(zero=False),
            color="space_names:N",
            column="space_names:N",
        )
    )
    base.show()


def get_case_surfaces():
    case = EneryPlusCaseEditor(
        DUMMY_OUTPUT_PATH, starting_path=GRAPHBEM_PATH / "out.idf"
    )
    pz = PlanZones(case.idf)
    surfs_list = chain_flatten([s.surfaces for s in pz.zones])
    surfs = {s.idf_name.upper(): s for s in surfs_list}
    return surfs


def decompose_surface_name(name: str):
    surfs = get_case_surfaces()
    surf = surfs[name.upper()]
    return {
        "zone": surf.dname.plan_name,
        "direction": surf.direction.name,
        "is_exterior": not surf.is_interior,
    }


def analyze_surfaces():
    sql_result = get_sql_results(GRAPHBEM_PATH)
    df = create_dataframe_for_case(CASE_NAME, sql_result, variables["SURF_OUT_TEMP"])
    rprint(df.head())

    df2 = (
        df.with_columns(
            pl.col("space_names")
            .map_elements(decompose_surface_name, pl.Struct)
            .alias("surface_name_decomp")
        )
        .unnest("surface_name_decomp")
        .filter(pl.col("is_exterior"))
    )

    base = (
        alt.Chart(df2)
        .mark_line()
        .encode(
            x="datetimes",
            y=alt.Y("mean(values)", title=variables["SURF_OUT_TEMP"]).scale(zero=False), # TODO add units.. 
            color="direction:N",
            column="zone:N",
        )
    )
    base.show()


if __name__ == "__main__":
    analyze_surfaces()
    # analyze_case()
