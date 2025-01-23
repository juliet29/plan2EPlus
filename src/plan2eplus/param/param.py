# each parameterization needs to map changes that will be effected at the correct time, and keep track of these changes so that the folder / case name can automatically be labeled.. 
# AND/OR use dumb names and somehow keep running tally of diffs from the base case, and save some kind of descriptor file... 

from collections import namedtuple
from enum import Enum
from ..helpers.geometry_interfaces import WallNormal
from ..helpers.helpers import sort_and_group_objects_dict
from ..plan.plan_to_eppy import ExtendedIDF
from ..subsurfaces.interfaces import SubsurfaceAttributes



## windows / doors.. 
def create_windows() -> list[SubsurfaceAttributes]:
    ...

def create_doors() -> list[SubsurfaceAttributes]:
    ...


class SurfaceMapping(Enum):
    # current paradigm assumes that there is only one window / door per surface, although this may change in future.. 
    ALL = 0 # need to assert only 1 object 
    NSEW = 1 # need to have 4
    NS_EW = 2 # need to have 2 
    EXT_INT = 3 # need to have 2, and this is only valid for doors, unless there are interior windows.. but also rn, only doing int doors.. 


def split_walls_by_azimuth(idf:ExtendedIDF):
    WallDir = namedtuple("WallDir", ["wall", "dir"])
    walls_and_dirs = [WallDir(i.Name, WallNormal(round(float(i.azimuth)))) for i in idf.getsurfaces()] # TODO make this cleaner.. 
    return sort_and_group_objects_dict(walls_and_dirs, lambda x: x.dir.value)


### door and window schedules.. could do a similar thing.. 
### constructions.. could do a similar thing also.., => passing objects that that match construction sets, and specifying a type of mapping.. could have even a more unique mapping function...

## for door and window attributes => the subsurface attributes are modified... 


# IDF extension needs to define list of windows+surface mapping, list of doors+surface mapping, and so on.. 
# maybe can also allow update fx, where select explicitly.. 
# will extrat info based on this.. 


# now have function that takes in the idf and gets the required objects..
# function at base compares pairs to see if they match the walls..



def apply_modifications(idf:ExtendedIDF, attributes:list[SubsurfaceAttributes], mapping:SurfaceMapping):
    if SurfaceMapping.NSEW | SurfaceMapping.NS_EW:
        surface_split = 0 # split walls by azimuth.. 
    match mapping:
        case SurfaceMapping.ALL:
            assert len(attributes) == 1
            # get all objects of the type, or subsurface lists, which may become a part of the extended idf, and assign.. 
        case SurfaceMapping.NSEW | SurfaceMapping.NS_EW:
            pass
            # split walls by azimuth
            # and assign 
        case SurfaceMapping.EXT_INT:
            pass