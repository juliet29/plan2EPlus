from case_edits.epcase import EneryPlusCaseEditor
from case_edits.methods.outputs import add_output_variable


def modify_outputs(case_name, outputs, starting_case="base/02twoRoom"):
    e = EneryPlusCaseEditor(case_name, starting_case)

    for var in outputs:
        e.idf = add_output_variable(e.idf, var)

    e.save_idf()
    e.prepare_to_run()

    return e

    

