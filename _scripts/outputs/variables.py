from enum import Enum


class OutputVars(str, Enum):
    # AFN ~ system
    zone_vent_vol = "AFN Zone Ventilation Volume"
    zone_ach = "AFN Zone Ventilation Air Change Rate"
    zone_vent_heat_gain = "AFN Zone Ventilation Sensible Heat Gain Rate"
    zone_vent_heat_loss = "AFN Zone Ventilation Sensible Heat Loss Rate"

    # AFN ~ node
    node_temp = "AFN Node Temperature"
    node_total_pressure = "AFN Node Total Pressure"
    node_wind_pressure = "AFN Node Wind Pressure"

    # AFN ~ linkage
    linkage_flow12 = "AFN Linkage Node 1 to Node 2 Volume Flow Rate"
    linkage_flow21 = "AFN Linkage Node 2 to Node 1 Volume Flow Rate"

    # AFN ~ surface
    surface_venting = "AFN Surface Venting Window or Door Opening Factor"

    # zone ~  rates
    zone_mean_air_temp = "Zone Mean Air Temperature"
    zone_surface_convection_heat_transfer = "Zone Air Heat Balance Surface Convection Rate"
    zone_interzone_heat_transfer = "Zone Air Heat Balance Interzone Air Transfer Rate"
    zone_outdoor_heat_transfer = "Zone Air Heat Balance Outdoor Air Transfer Rate"
    zone_energy_balance = "Zone Air Heat Balance Air Energy Storage Rate"

    # surface ~ face ~ rates / area 
    inside_face_convection_heat_gain = 'Surface Inside Face Convection Heat Gain Rate per Area' 
    inside_face_net_surface_thermal_radiation_heat_gain = 'Surface Inside Face Net Surface Thermal Radiation Heat Gain Rate per Area' 
    inside_face_solar_radiation_heat_gain = 'Surface Inside Face Solar Radiation Heat Gain Rate per Area' 
    inside_face_internal_gains_radiation = 'Surface Inside Face Internal Gains Radiation Rate per Area' 
    average_face_conduction_heat_transfer = "Surface Average Face Conduction Heat Transfer Rate per Area"





    # site
    site_db_temp = "Site Outdoor Air Drybulb Temperature"
    site_wb_temp = "Site Outdoor Air Wetbulb Temperature"
    site_dp_temp = "Site Outdoor Air Dewpoint Temperature"
    site_direct_solar_rad = "Site Direct Solar Radiation Rate per Area"
    site_diffuse_solar_rad = "Site Diffuse Solar Radiation Rate per Area"
    site_solar_angle = "Site Solar Azimuth Angle"
    site_wind_speed = "Site Wind Speed"
    site_wind_direction = "Site Wind Direction"

    # outside surface
    surf_incident_solar_rad = (
        "Surface Outside Face Incident Solar Radiation Rate per Area"
    )
    surf_net_thermal_rad = (
        "Surface Outside Face Net Thermal Radiation Heat Gain Rate per Area"
    )
    surf_outside_temp = "Surface Outside Face Temperature"

    # inside surface
    surf_inside_temp = "Surface Inside Face Temperature"
    


# access name by value
class PostProcessedOutputVars(str, Enum):
    zone_vent_net_heat_loss = "Zone Ventilation Net Heat Loss"