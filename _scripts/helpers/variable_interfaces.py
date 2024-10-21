from variables import afn, surface, site, zone
from dataclasses import dataclass
from helpers.helpers import chain_flatten


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


@dataclass
class SurfaceVariablesPattern(Vars):
    rate_per_area: dict
    temp: dict


@dataclass
class SurfaceVariables(Vars):
    inside_face: SurfaceVariablesPattern
    outside_face: SurfaceVariablesPattern
    average_face: SurfaceVariablesPattern


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
surface_vars = {k: SurfaceVariablesPattern(*v) for k, v in surface.items()}
surface_vars = SurfaceVariables(**surface_vars)

all_variables = AllVariables(
    **{"afn": afn_vars, "zone": zone_vars, "surface": surface_vars, "site": site_vars}
)

def get_vars(arr: list[AFNVariables | ZoneVariables | SiteVariables]=[afn_vars, zone_vars, site_vars]):
    vars = []
    for a in arr:
        vars.append(a.get_values())
    return chain_flatten(vars)