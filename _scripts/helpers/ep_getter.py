from __future__ import annotations
import re
from typing import Union

from geomeppy import IDF
import case_edits.epcase as epcase
from methods.subsurfaces.pairs import SubsurfaceObjects


class Getter:
    def __init__(self, epcase_or_idf:Union[epcase.EneryPlusCaseEditor, IDF]) -> None:
        if type(epcase_or_idf) == epcase.EneryPlusCaseEditor:
            self.idfobjects = epcase_or_idf.idf.idfobjects
        elif type(epcase_or_idf) == IDF:
            self.idfobjects = epcase_or_idf.idfobjects

        self.subsurfaces = []

    def get_original_subsurfaces(self):
        if not self.subsurfaces:
            self.get_subsurfaces()
        self.original_subsurfaces = [
            s for s in self.subsurfaces if "Partner" not in s.Name
        ]
        return self.original_subsurfaces

    def get_subsurfaces(self):
        types = [SubsurfaceObjects(i).name for i in range(2)]
        for type in types:
            pattern = re.compile(type)
            self.get_subsurface_by_type(pattern)
        return self.subsurfaces

    def get_subsurface_by_type(self, pattern):
        for k, v in self.idfobjects.items():
            if bool(pattern.match(k)):
                if len(v) > 0:
                    for item in v:
                        if "Building_Surface_Name" in item.fieldnames:
                            self.subsurfaces.append(item)

    # TODO repetitive..
    def get_afn_objects(self):
        self.afn_objects = []
        pattern = re.compile("AIRFLOWNETWORK")
        for k, v in self.idfobjects.items():
            if bool(pattern.match(k)):
                if len(v) > 0:
                    for item in v:
                        self.afn_objects.append(item)
        return self.afn_objects
