from dataclasses import dataclass
from helpers.variables import afn, surface, site, zone
from helpers.helpers import chain_flatten

def get_values(d:dict):
        return chain_flatten([list(v.values()) for v in d.values()])

@dataclass
class Vars:
    def get_values(self):
        return chain_flatten([list(v.values()) for v in self.__dict__.values()])
    

@dataclass
class AFNVariables(Vars):
    zone: dict
    node: dict
    linkage: dict
    surface: dict


@dataclass
class ZoneVariables(Vars):
    temp: dict
    rate: dict
    wind: dict


@dataclass
class SurfaceVariablesPattern(Vars):
    rate_per_area: dict
    temp: dict


@dataclass
class SurfaceVariables(Vars):
    inside_face: dict
    outside_face: dict
    average_face: dict


@dataclass
class SiteVariables(Vars):
    temp: dict
    solar: dict
    wind: dict


@dataclass
class AllVariables(Vars):
    afn: AFNVariables
    zone: ZoneVariables
    surface: SurfaceVariables
    site: SiteVariables


afn_vars = AFNVariables(**afn)
zone_vars = ZoneVariables(**zone)
site_vars = SiteVariables(**site)

surface_vars = SurfaceVariables(**surface)

all_variables = AllVariables(
    **{"afn": afn_vars, "zone": zone_vars, "surface": surface_vars, "site": site_vars}
)

def get_vars(arr: list[AFNVariables | ZoneVariables | SiteVariables |SurfaceVariables]=[afn_vars, zone_vars, site_vars, surface_vars]):
    vars = []
    for a in arr:
        if hasattr(a, "inside_face"):
            for v in a.__dict__.values():
                vars.append(get_values(v))

        else:
            vars.append(a.get_values())

    
    return chain_flatten(vars)