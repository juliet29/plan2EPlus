from typing import Optional
from dataclasses import dataclass
from geomeppy import IDF


@dataclass
class IDFModifications:
    height: float = 3.05 #m
    window_area: Optional[dict] = None # if it exists, either a single value or a function mapping changes to room edges.. 
    
class ExtendedIDF(IDF):
    def __init__(self, idfname=None, epw=None, modifications:IDFModifications=IDFModifications()):
        super().__init__(idfname, epw)
        self.modifications = modifications