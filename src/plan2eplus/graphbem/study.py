from plan2eplus.constants import SRC_PATH, DUMMY_OUTPUT_PATH
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.case_edits.ezcase import add_rooms, finish_creating_ezcase
from plan2eplus.visuals.interfaces import PlanZones

from plan2eplus.subsurfaces.interfaces import (
    NinePointsLocator,
    SubsurfaceAttributes,
    SubsurfaceObjects,
    SubsurfacePair,
)


# NOTES -> no AFN + some single sided ventilation... 


input_path = SRC_PATH / "graphbem"

# windows.. 





def test_graph_bem():
    case = EneryPlusCaseEditor(DUMMY_OUTPUT_PATH)
    case.idf = add_rooms(case.idf, input_path)
    pz = PlanZones(case.idf)
    pz.plot_zone_domains()
    # case.idf.printidf()
    # pz.zones[0].get_plan_name(input_path)




if __name__ == "__main__":
    print("Running connectivity test..")
    test_graph_bem()
