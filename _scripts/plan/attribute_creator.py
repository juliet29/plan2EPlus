from methods.subsurfaces.pairs import SubsurfaceAttributes, SubsurfaceObjects
from methods.dynamic_subsurfaces.inputs import (
    Dimensions,
    NinePointsLocator,
)
from helpers.dimensions import nice_dim
from plan.interfaces import SubSurfacesJSON, WindowsJSON, DoorsJSON



def create_subsurface_database(subsurfaces:SubSurfacesJSON, object_type: SubsurfaceObjects, location: NinePointsLocator):
    def create_attributes(item: DoorsJSON | WindowsJSON):
        return SubsurfaceAttributes(
            object_type=object_type,
            construction=None,
            dimensions=get_dimensions(item),
            location_in_wall=location,
        )
    ot = "WINDOWS" if object_type == SubsurfaceObjects.WINDOW else "DOORS"
    return {item["id"]: create_attributes(item) for item in subsurfaces[ot]}


def get_dimensions(item: DoorsJSON | WindowsJSON):
    w, h = item["width"], item["height"]
    return Dimensions(float(w), float(h))


# but is this even correct? bc need to dynamically adjust window and door sizes.. 


# class AttributeCreator:
#     def __init__(self, subsurfaces:SubSurfacesJSON) -> None:
#         self.subsurfaces = subsurfaces

#     def run(self):
#         self.create_windows()
#         self.create_doors()


#     def create_windows(self):
#         self.window_db = {}
#         for item in self.subsurfaces["WINDOWS"]:
#             self.window_db[item["id"]] = SubsurfaceAttributes(
#                 object_type=SubsurfaceObjects.WINDOW,
#                 construction=None,
#                 dimensions=self.get_dimensions(item),
#                 location_in_wall=NinePointsLocator.top_middle,
#             )


#     def create_doors(self):
#         self.door_db = {}
#         for item in self.subsurfaces["DOORS"]:
#             self.door_db[item["id"]] = SubsurfaceAttributes(
#                 object_type=SubsurfaceObjects.DOOR,
#                 construction=None,
#                 dimensions=self.get_dimensions(item),
#                 location_in_wall=NinePointsLocator.bottom_middle,
#             )



#     # # TODO this def supposed to be somewhere else.. 
#     # def get_height(self):
#     #     self.heights = []
#     #     floor_height = self.subsurfaces["FLOOR_HEIGHT"]
#     #     if str(floor_height):
#     #         self.heights.append(nice_dim(floor_height))
#     #     else:
#     #         for item in self.subsurfaces["FLOOR_HEIGHT"]:
#     #             print(item)
#     #             self.heights.append(nice_dim(item))
