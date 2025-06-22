from geomeppy import IDF
from plan2eplus.constants import PATH_TO_DUMMY_OUTPUTS
from plan2eplus.case_edits.epcase import EneryPlusCaseEditor
from plan2eplus.connectivity_study.study import output_path as graph2plan_idf_path
from rich import print as rprint

from plan2eplus.visuals.interfaces import PlanZones


def create_plan(idf: IDF):
    pass
    # rprint(idf.__dict__.keys())
    # p = PlanZones(idf)
    # p.zones[0].dname
    # p.plot_zone_domains()
    # zones = [Zone(obj) for obj in get_zones(idf)]
    # rprint(zones[2].subsurfaces)
    # for surface in zones[1].surfaces:
    #     surface.subsurfaces
    # print(zones[0].dname)

    # surfaces = [Surface(obj) for obj in get_surfaces(idf)]
    # # for s in surfaces:
    # #     s.domain

    # # print(surfaces)

    # # print(surfaces[0].ep_object.unit_normal)
    # # pprint([i.nickname for i in surfaces])

    # subsurfaces = [Subsurface(obj) for obj in idf.getsubsurfaces()]
    # pprint([i.nickname for i in subsurfaces])

    # zone_dict = {i.idf_name:i for i in zones}
    # surface_dict = {i.idf_name:i for i in surfaces}
    # subsurface_dict = {i.idf_name:i for i in subsurfaces}

    # plan = Plan(zone_dict, surface_dict, subsurface_dict)

    # print(list(plan.subsurfaces.values())[0].ep_object)
    # print(list(plan.surfaces.values())[0].ep_object)
    # print(plan.surfaces)


def create_subsurfaces(idf: IDF):
    pass


if __name__ == "__main__":
    case = EneryPlusCaseEditor(
        path_to_outputs=PATH_TO_DUMMY_OUTPUTS,
        starting_path=graph2plan_idf_path / "out.idf",
    )
    print("\n---testing visual initialization.. ---")
    create_plan(case.idf)
