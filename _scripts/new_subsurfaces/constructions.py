from geomeppy import IDF
from new_subsurfaces.interfaces import SubsurfaceAttributes, SubsurfaceObjects


def assign_default_constructions(idf: IDF, attrs: SubsurfaceAttributes):
    try:
        door_const = idf.getobject("CONSTRUCTION", "Project Door")
        window_const = idf.getobject("CONSTRUCTION", "Project External Window")
    except:
        raise Exception("Need to set default constructions")

    if attrs.object_type == SubsurfaceObjects.DOOR:
        attrs.construction = door_const
    else:
        attrs.construction = window_const

    return attrs