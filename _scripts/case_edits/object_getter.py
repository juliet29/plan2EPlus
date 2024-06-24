import re

# from case_edits.epcase import EneryPlusCaseEditor
from case_edits.methods.subsurfaces.inputs import SubsurfaceObjects

class Getter:
    def __init__(self, epcase) -> None:
        self.epcase = epcase
        self.subsurfaces = []

    def get_original_subsurfaces(self):
        self.original_subsurfaces = [s for s in self.subsurfaces if "Partner" not in s.Name]
        return self.original_subsurfaces


    def get_subsurfaces(self):
        types = [SubsurfaceObjects(i).name for i in range(2)]
        for type in types:
            pattern = re.compile(type)
            self.get_subsurface_by_type(pattern)
        return self.subsurfaces


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
        return self.afn_objects