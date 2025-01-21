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


# IDF extension needs to define list of windows+surface mapping, list of doors+surface mapping, and so on.. 
# maybe can also allow update fx, where select explicitly.. 
# will extrat info based on this.. 


# now have function that takes in the idf and gets the required objects..
# function at base compares pairs to see if they match the walls..
