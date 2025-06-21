from dataclasses import dataclass
from pathlib import Path
from .variables import afn, surface, site, zone
from .helpers import chain_flatten, load_data_from_json


def get_values(d:dict):
        return chain_flatten([list(v.values()) for v in d.values()])

@dataclass
class Vars:
    def get_values(self):
        return chain_flatten([list(v.values()) for v in self.__dict__.values()])
    

@dataclass
class AFNVariables(Vars):
    zone: dict[str,str]
    node: dict[str,str]
    linkage: dict[str,str]
    surface: dict[str,str]


@dataclass
class ZoneVariables(Vars):
    temp: dict[str,str]
    rate: dict[str,str]
    wind: dict[str,str]


@dataclass
class SurfaceVariablesPattern(Vars):
    rate_per_area: dict[str,str]
    temp: dict[str,str]


@dataclass
class SurfaceVariables(Vars):
    inside_face: dict[str,str]
    outside_face: dict[str,str]
    average_face: dict[str,str]


@dataclass
class SiteVariables(Vars):
    temp: dict[str,str]
    solar: dict[str,str]
    wind: dict[str,str]


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



def prepare_to_load_additional_variables_from_file(path: Path):
    def get_additional_variables():
        variables:list[str] = load_data_from_json(path.parent, path.name)
        return variables

    return get_additional_variables