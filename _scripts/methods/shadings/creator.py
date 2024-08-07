from geomeppy import IDF
from geometry.subsurface import Subsurface

class ShadingCreator:
    def __init__(self, subsurface_name:str, case_idf:IDF) -> None:
        self.subsurface_name = subsurface_name
        self.case_idf = case_idf
        self.tilt_angle = 70 # degrees
        self.shading_height_above_subsurface = 0.01 # m
        self.depth = 3 # m


    def run(self):
        self.create_shading_name()
        self.create_shading()

    def create_shading_name(self):
        self.name = f"{self.subsurface_name} Shading"

    def create_shading(self):
        self.shading = self.case_idf.newidfobject("SHADING:OVERHANG")
        self.shading.Name = self.name
        self.shading.Window_or_Door_Name = self.subsurface_name
        self.shading.Tilt_Angle_from_WindowDoor = self.tilt_angle
        self.shading.Height_above_Window_or_Door = self.shading_height_above_subsurface
        self.shading.Depth = self.depth
        self.shading.Left_extension_from_WindowDoor_Width = 0
        self.shading.Right_extension_from_WindowDoor_Width = 0






