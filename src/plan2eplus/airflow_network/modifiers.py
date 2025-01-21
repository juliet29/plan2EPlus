from copy import deepcopy
from geomeppy import IDF

def add_simulation_control(idf: IDF):
    sim_control = idf.newidfobject(
        "AirflowNetwork:SimulationControl".upper()
    )
    sim_control.Name = "AFN_SIM_CONTROL"
    sim_control.AirflowNetwork_Control = "MultizoneWithoutDistribution"
    return idf


def add_zone(idf: IDF, zone_name:str):
    zone = idf.newidfobject(
        "AirflowNetwork:MultiZone:Zone".upper()
    )
    zone.Ventilation_Control_Mode = "Constant"
    zone.Zone_Name = zone_name
    return idf

def create_simple_opening(idf: IDF, subsurface_name:str):
    opening = idf.newidfobject(
        "AirflowNetwork:MultiZone:Component:SimpleOpening".upper()
    )
    opening.Name = f"{subsurface_name} SimpleOpening"
    # taken from defaults
    opening.Discharge_Coefficient = 1
    opening.Air_Mass_Flow_Coefficient_When_Opening_is_Closed = 0.001
    opening.Minimum_Density_Difference_for_TwoWay_Flow = 0.0001
    return idf, opening

def add_subsurface(idf: IDF, subsurface_name:str):
    afn_surface = idf.newidfobject(
        "AirflowNetwork:MultiZone:Surface".upper()
    )
    afn_surface.Surface_Name = subsurface_name

    idf, opening = create_simple_opening(idf, subsurface_name)
    afn_surface.Leakage_Component_Name = opening.Name
    return idf


