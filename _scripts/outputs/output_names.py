from enum import Enum

class OutputVariables(str, Enum):
    # zone 
    zone_mean_air_temp = 'Zone Mean Air Temperature'

    # site 
    site_db_temp = "Site Outdoor Air Drybulb Temperature"
    site_wb_temp = "Site Outdoor Air Wetbulb Temperature"
    direct_solar_rad_rate = "Site Direct Solar Radiation Rate per Area"

# access name by value 