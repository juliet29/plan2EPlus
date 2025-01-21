from airflow_network.logic import get_afn_zones_and_subsurfaces
from airflow_network.modifiers import add_simulation_control, add_subsurface, add_zone


from geomeppy import IDF
from copy import deepcopy


def add_airflownetwork_to_case(_idf: IDF):
    idf = deepcopy(_idf)
    zones, subsurfaces = get_afn_zones_and_subsurfaces(idf)

    idf = add_simulation_control(idf)

    for zone in zones:
        idf = add_zone(idf, zone)

    for subsurface in subsurfaces:
        idf = add_subsurface(idf, subsurface)

    return idf
