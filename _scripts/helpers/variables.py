afn = {
    "zone": {
        "vent_vol": "AFN Zone Ventilation Volume",
        "mix_vol": "AFN Zone Mixing Volume",
        "vent_heat_gain": "AFN Zone Ventilation Sensible Heat Gain Rate",
        "vent_heat_loss": "AFN Zone Ventilation Sensible Heat Loss Rate",
        "vent_heat_gain_latent": "AFN Zone Ventilation Latent Heat Gain Rate",
        "vent_heat_loss_latent": "AFN Zone Ventilation Latent Heat Loss Rate",
        "mix_heat_gain": "AFN Zone Mixing Sensible Heat Gain Rate",
        "mix_heat_loss": "AFN Zone Mixing Sensible Heat Loss Rate",
        "mix_heat_gain_latent": "AFN Zone Mixing Latent Heat Gain Rate",
        "mix_heat_loss_latent": "AFN Zone Mixing Latent Heat Loss Rate",
        "ach": "AFN Zone Ventilation Air Change Rate",
    },
    "node": {
        "temp": "AFN Node Temperature",
        "total_pressure": "AFN Node Total Pressure",
        "wind_pressure": "AFN Node Wind Pressure",
    },
    "linkage": {
        "flow12": "AFN Linkage Node 1 to Node 2 Volume Flow Rate",
        "flow21": "AFN Linkage Node 2 to Node 1 Volume Flow Rate",
    },
    "surface": {
        "opening_factor": "AFN Surface Venting Window or Door Opening Factor",
    },
}


zone = {
    "temp": {
        "zone_mean_air_temp": "Zone Mean Air Temperature",
    },
    "rate": {
        "surface_convection": "Zone Air Heat Balance Surface Convection Rate",
        "interzone_heat_transfer": "Zone Air Heat Balance Interzone Air Transfer Rate",
        "outdoor_heat_transfer": "Zone Air Heat Balance Outdoor Air Transfer Rate",
        "energy_storage": "Zone Air Heat Balance Air Energy Storage Rate",
    },
    "wind": {
        "speed": "Zone Outdoor Air Wind Speed",
        "direction": "Zone Outdoor Air Wind Direction",
    }
}

surface = {
    "inside_face": {
        "rate_per_area": {
            "convection_heat_gain": "Surface Inside Face Convection Heat Gain Rate per Area",
            "net_surface_thermal_radiation_heat_gain": "Surface Inside Face Net Surface Thermal Radiation Heat Gain Rate per Area",
            "solar_radiation_heat_gain": "Surface Inside Face Solar Radiation Heat Gain Rate per Area",
            "internal_gains_radiation": "Surface Inside Face Internal Gains Radiation Rate per Area",
        },
        "temp": {
            "surf_inside_temp": "Surface Inside Face Temperature",
        },
    },
    "average_face": {
        "rate_per_area": {
            "conduction_heat_transfer": "Surface Average Face Conduction Heat Transfer Rate per Area",
        },
        "temp": {},
    },
    "outside_face": {
        "rate_per_area": {
            "surf_incident_solar_rad": "Surface Outside Face Incident Solar Radiation Rate per Area",
            "surf_net_thermal_rad": "Surface Outside Face Net Thermal Radiation Heat Gain Rate per Area",
        },
        "temp": {
            "temp": "Surface Outside Face Temperature",
        },
        "wind": {
            "speed": "Surface Outside Face Outdoor Air Wind Speed",
            "direction": "Surface Outside Face Outdoor Air Wind Direction"
        }
    },
}


site = {
    "temp": {
        "db": "Site Outdoor Air Drybulb Temperature",
        "wb": "Site Outdoor Air Wetbulb Temperature",
        "dp": "Site Outdoor Air Dewpoint Temperature",
    },
    "solar": {
        "direct_rad": "Site Direct Solar Radiation Rate per Area",
        "diffuse_rad": "Site Diffuse Solar Radiation Rate per Area",
        "solar_angle": "Site Solar Azimuth Angle",
    },
    "wind": {
        "speed": "Site Wind Speed",
        "direction": "Site Wind Direction",
    },
}

