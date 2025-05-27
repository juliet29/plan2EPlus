from plan2eplus.config import PATH_TO_GRAPH2PLAN_CASES, PATH_TO_OUTPUT_CASES
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import add_rooms

output_path = PATH_TO_OUTPUT_CASES / "250527_threeplan"
input_path = PATH_TO_GRAPH2PLAN_CASES / "three_plan"


def test_connectivity_cases():
    case = EneryPlusCaseEditor(
        output_path
    )
    case.idf = add_rooms(case.idf, input_path, "path.json")
    case.idf.printidf()

    return 


if __name__ == "__main__":
    print("Running connectivity test..")
    test_connectivity_cases()