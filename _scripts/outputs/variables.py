from enum import Enum


class OutputVars(str, Enum):
    # AFN ~ system 
    zone_vent_vol = "AFN Zone Ventilation Volume"
    zone_ach = "AFN Zone Ventilation Air Change Rate"
    zone_vent_heat_gain = "AFN Zone Ventilation Sensible Heat Gain Rate"

    # AFN ~ node 
    node_temp = "AFN Node Temperature"
    node_total_pressure = "AFN Node Total Pressure"
    node_wind_pressure = "AFN Node Wind Pressure"
    
    # AFN ~ linkage 
    linkage_flow = "AFN Linkage Node 1 to Node 2 Volume Flow Rate"
    
    # AFN ~ surface 
    surface_venting = "AFN Surface Venting Window or Door Opening Factor"

    # zone
    zone_mean_air_temp = "Zone Mean Air Temperature"

    # site
    # https://bigladdersoftware.com/epx/docs/22-2/input-output-reference/group-location-climate-weather-file-access.html#outputs-3-011
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

    # inside surface
    in_surf_temp = "Surface Inside Face Temperature"


# access name by value
