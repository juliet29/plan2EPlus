import re

from case_edits.epcase import EneryPlusCaseEditor
from case_edits.methods.subsurfaces.subsurface import SubsurfaceType

class Getter:
    def __init__(self, epcase:EneryPlusCaseEditor) -> None:
        self.epcase = epcase
        self.subsurfaces = []

    # TODO move elsewhere .. 
    def get_subsurfaces(self):
        types = [SubsurfaceType(i).name for i in range(2)]
        for type in types:
            pattern = re.compile(type)
            self.get_subsurface_by_type(pattern)


    def get_subsurface_by_type(self, pattern):
        for k,v in self.epcase.idf.idfobjects.items():
            if bool(pattern.match(k)):
                if len(v) > 0:
                    for item in v:
                        if "Building_Surface_Name" in item.fieldnames:
                            self.subsurfaces.append(item)

    # TODO repetitive.. 
    def get_afn_objects(self):
        self.afn_objects = []
        pattern = re.compile("AIRFLOWNETWORK")
        for k,v in self.epcase.idf.idfobjects.items():
            if bool(pattern.match(k)):
                if len(v) > 0:
                    for item in v:
                        self.afn_objects.append(item)