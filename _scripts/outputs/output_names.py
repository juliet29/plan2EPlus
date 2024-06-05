from enum import Enum

class OutputVariables(str, Enum):
    # zone 
    zone_mean_air_temp = 'Zone Mean Air Temperature'

    # site 
    db_temp = "Site Outdoor Air Drybulb Temperature"
    wb_temp = "Site Outdoor Air Wetbulb Temperature"
    dp_temp = "Site Outdoor Air Dewpoint Temperature"
    direct_solar_rad = "Site Direct Solar Radiation Rate per Area"
    diffuse_solar_rad = "Site Diffuse Solar Radiation Rate per Area"
    solar_angle = "Site Solar Azimuth Angle"


# access name by value 