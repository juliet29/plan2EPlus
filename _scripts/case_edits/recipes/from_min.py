from case_edits.epcase import EneryPlusCaseEditor
from case_edits.methods.outputs import add_output_variable, request_sql



WEST_COORDS = [(5,0), (5,7), (0,7), (0,0)]
NORTH_COORDS = [(10,7), (10,11), (0,11), (0,7)]

def create_case(case_name, outputs, run=False):
    e = EneryPlusCaseEditor(case_name)

    e.idf.add_block(
      name='North',
      coordinates=NORTH_COORDS,
      height=3
    )
    e.idf.add_block(
      name='West',
      coordinates=WEST_COORDS,
      height=3
    )

    e.get_geometry()

    e.idf = request_sql(e.idf)

    for var in outputs:
        e.idf = add_output_variable(e.idf, var)

    e.save_idf()
    e.prepare_to_run()

    if run:
        e.run_idf()

    return e