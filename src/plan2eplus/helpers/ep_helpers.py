from geomeppy import IDF
from eppy.bunch_subclass import EpBunch
from plan2eplus.helpers.geometry_interfaces import WallNormal
from plan2eplus.visuals.idf_name import IDFName, decompose_idf_name

### for surfaces..


def get_first_object(idf: IDF, idfobject: str, IS_UNIQUE=True):
    idfobjects = idf.idfobjects[idfobject]
    if IS_UNIQUE:
        assert len(idfobjects) == 1
    return idfobjects[0]


## IDF and objects generally
def show_idf_keys(idf: IDF):
    print(idf.idfobjects.keys())


def show_object_attributes(ep_object: EpBunch):
    print(ep_object.__dict__)


## Zones ----


def get_zone_num(name: str):
    return int(name.split(" ")[1])


def get_zones(idf: IDF) -> list[EpBunch]:
    return [i for i in idf.idfobjects["ZONE"]]


def get_zone_name_by_num(idf: IDF, num: int):
    zone_names = [decompose_idf_name(i.Name) for i in get_zones(idf)]
    name = [i for i in zone_names if i.zone_number == num]
    assert len(name) == 1, (
        f"No zone with number `{num}` in {[n.recreate_zone_name for n in name]}"
    )
    return name[0].recreate_zone_name

    # return f"Block 0{num} Storey 0"  # TODO to not break rest of code, going to break Plan Zones.. 5/31/25 8:17pm


def get_zone_by_name(idf: IDF, name: str):
    return idf.getobject("ZONE", name)


## Surfaces ----


def get_surfaces(idf: IDF) -> list[EpBunch]:
    return [i for i in idf.idfobjects["BUILDINGSURFACE:DETAILED"]]


# TODO refactor this significantlu..
def get_zone_walls_by_zone_num(idf: IDF, num: int) -> list[EpBunch]:
    return [
        i
        for i in idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        if get_zone_name_by_num(idf, num) in i.Name and "Wall" in i.Name
    ]


# can alse do zone.zonesubusrfaces then filter to walls ..


def get_surface_direction(idf: IDF, surface_name: str):
    surface = idf.getobject("BUILDINGSURFACE:DETAILED", surface_name)
    assert surface
    rounded_azimuuth = round(float(surface.azimuth))
    return WallNormal(rounded_azimuuth)


def is_interior_wall(surf: EpBunch):
    return surf.Surface_Type == "wall" and surf.Outside_Boundary_Condition == "surface"


def get_surface_by_name(idf: IDF, name):
    return idf.getobject("BUILDINGSURFACE:DETAILED", name)


def get_partner_of_surface(idf: IDF, surf: EpBunch):
    assert is_interior_wall  # TODO is this an error?
    return get_surface_by_name(idf, surf.Outside_Boundary_Condition_Object)


PARTNER = " Partner"


def create_partner_name(name: str):
    return name + PARTNER


def reverse_partner_name(partner_name: str):
    return partner_name.replace(PARTNER, "")


def get_surface_of_subsurface(idf: IDF, subsurface: EpBunch):
    return idf.getobject("BUILDINGSURFACE:DETAILED", subsurface.Building_Surface_Name)


def get_subsurface_by_name(idf: IDF, name: str):
    subsurfaces = idf.getsubsurfaces()
    return [i for i in subsurfaces if name == i.Name][0]


def find_zone_subsurfaces(zone_name: str, subsurfaces: list[EpBunch]) -> list[str]:
    return [s.Name for s in subsurfaces if zone_name in s.Building_Surface_Name]


def create_zone_map(idf: IDF) -> dict[str, list[str]]:
    zones = get_zones(idf)
    subsurfaces = idf.getsubsurfaces()
    # modify to include walls..
    return {z.Name: find_zone_subsurfaces(z.Name, subsurfaces) for z in zones}


def create_zone_map_without_partners(idf: IDF):
    zone_map = create_zone_map(idf)
    for k, v in zone_map.items():
        for ix, name in enumerate(v):
            if PARTNER in name:
                zone_map[k][ix] = reverse_partner_name(name)
    return zone_map


def get_subsurface_wall_num(name: str):
    temp = name.split(" ")[-2]
    res = temp.split("_")
    if len(res) == 1:
        return int(res[0])
    elif len(res) == 2:
        r = int(res[0])
        s = int(res[1])
        return float(f"{r}.{s}")
    else:
        raise Exception(f"Invalid name: {name}")


def get_surface_wall_num(name: str):
    temp = name.split(" ")[-1]
    res = temp.split("_")
    if len(res) == 1:
        return int(res[0])
    elif len(res) == 2:
        r = int(res[0])
        s = int(res[1])
        return float(f"{r}.{s}")
    else:
        raise Exception(f"Invalid name: {name}")


def get_simple_name_for_subsurface_or_wall(name: str):
    try:
        wall_num = get_subsurface_wall_num(name)
        type = name.split(" ")[-1][:3].lower()
    except:
        wall_num = get_surface_wall_num(name)
        type = "wall".upper()
    zone_num = get_zone_num(name)
    return f"b{zone_num}_{type}_{wall_num}"


def get_object_type(obj: EpBunch):
    return obj.objidd[0]["idfobj"]


def get_original_subsurfaces(idf):
    return [i for i in idf.getsubsurfaces() if PARTNER not in i.Name]
