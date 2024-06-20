import json

from case_edits.epcase import EneryPlusCaseEditor
from case_edits.methods.outputs import add_output_variable, request_sql

from gplan.convert import GPLANtoGeomeppy


def create_case(case_name, outputs, gplans_path, plan_index, run=False):

    with open(gplans_path) as f:
        gplan_data = json.load(f)
    floor_plan = gplan_data[plan_index]
    gg = GPLANtoGeomeppy(floor_plan)

    e = EneryPlusCaseEditor(case_name, starting_case="")
    for block in gg.blocks:
        e.idf.add_block(**block)

    e.get_geometry()

    e.idf = request_sql(e.idf)
    for var in outputs:
        e.idf = add_output_variable(e.idf, var)

    e.save_idf()
    e.prepare_to_run()

    if run:
        e.run_idf()

    return e, gg
