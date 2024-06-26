from enum import Enum


class OutputVars(str, Enum):
    # zone
    zone_mean_air_temp = "Zone Mean Air Temperature"
    zone_vent_vol = "AFN Zone Ventilation Volume"
    zone_ach = "AFN Zone Ventilation Air Change Rate"
    zone_vent_heat_gain = "AFN Zone Ventilation Sensible Heat Gain Rate"

    # site
    site_db_temp = "Site Outdoor Air Drybulb Temperature"
    site_wb_temp = "Site Outdoor Air Wetbulb Temperature"
    site_dp_temp = "Site Outdoor Air Dewpoint Temperature"
    site_direct_solar_rad = "Site Direct Solar Radiation Rate per Area"
    site_diffuse_solar_rad = "Site Diffuse Solar Radiation Rate per Area"
    site_solar_angle = "Site Solar Azimuth Angle"

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
