from eppy.bunch_subclass import EpBunch
from helpers.ep_helpers import get_object_type
from helpers.helpers import ContainsAsEqualsString


def init_cons_assignment():
    return {
        "exterior": "",
        "interior": "",
        "floor": "",
        "roof": "",
        "door": "",
        "window": "",
    }


def organize_cons(cons: EpBunch, cons_assignment: dict):
    cstring = ContainsAsEqualsString(cons.Name.lower())
    match cstring:
        case "exterior":
            key = "exterior"
        case "partitions":
            key = "interior"
        case "floor":
            key = "floor"
        case "roof":
            key = "roof"
        case "furnishings":
            key = "door"
        case "window":
            key = "window"
        case _:
            raise Exception(
                f"{cons.Name.lower()} has no overlap with cons_assignment keys: {cons_assignment.keys()}"
            )
    cons_assignment[key] = cons.Name
    return cons_assignment


def organize_cons_set(cons_set: list[EpBunch]):
    cons_assignment = init_cons_assignment()
    for cons in cons_set:
        cons_assignment = organize_cons(cons, cons_assignment)
    return cons_assignment


def match_surfaces(surface: EpBunch):
    try:
        _ = surface.Surface_Type
    except:
        return ""
    match surface.Surface_Type.lower():
        case "wall":
            return (
                "exterior"
                if surface.Outside_Boundary_Condition.lower() == "outdoors"
                else "interior"
            )
        case "floor":
            return "floor"
        case "roof":
            return "roof"
        case _:
            return ""


def match_subsurfaces(surface: EpBunch):
    obj_type = get_object_type(surface)
    cstring = ContainsAsEqualsString(obj_type.lower())
    match cstring:
        case "door":
            return "door"
        case "window":
            return "window"
        case _:
            return ""


def assign_material_to_surface(surface: EpBunch, cons_assignment: dict):
    key = match_surfaces(surface)
    if not key:
        key = match_subsurfaces(surface)
    if not key:
        otype = get_object_type(surface)
        raise Exception(
            f"No match for {surface.Surface_Type} of  {surface.Name} with {otype}"
        )
    if cons_assignment[key]:
        surface.Construction_Name = cons_assignment[key]
    else:
        print(f"key: {key} -> val: {cons_assignment[key]} has not been assigned!")
    return
