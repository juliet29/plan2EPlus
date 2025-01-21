from geomeppy import IDF
from subsurfaces.interfaces import SubsurfaceAttributes, SubsurfaceObjects


def assign_default_constructions(idf: IDF, attrs: SubsurfaceAttributes):
    try:
        door_const = idf.getobject("CONSTRUCTION", "Project Door")
        window_const = idf.getobject("CONSTRUCTION", "Project External Window")
    except:
        raise Exception("Need to set default constructions")

    # print("attrs in constr", attrs.object_type)
    if attrs.object_type == SubsurfaceObjects.DOOR:
        # print("hi im a door")
        attrs.construction = door_const
    else:
        # print("hi im a window")
        attrs.construction = window_const

    return attrs
