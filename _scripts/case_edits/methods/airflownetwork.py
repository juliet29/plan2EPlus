from case_edits.epcase import EneryPlusCaseEditor
from case_edits.object_getter import Getter


class AirflowNetwork:
    def __init__(self, epcase:EneryPlusCaseEditor) -> None:
        self.epcase = epcase

    def create_simulation_control(self):
        self.sim_control = self.epcase.idf.newidfobject("AirflowNetwork:SimulationControl".upper())
        self.sim_control.Name = "AFN_SIM_CONTROL"
        self.sim_control.AirflowNetwork_Control = "MultizoneWithoutDistribution"


    def create_zone_objects(self):
        for thermal_zone in self.epcase.geometry.zones.values():
            self.zone = self.epcase.idf.newidfobject("AirflowNetwork:MultiZone:Zone".upper())
            self.zone.Ventilation_Control_Mode = "Constant"
            self.zone.Zone_Name = thermal_zone.name
            # self.zone.Venting_Availability_Schedule_Name = 0
            # Venting Availability Schedule Name is left blank, signifying always open, when 0 => doors are closed.. 


    def create_zone_surfaces(self):
        self.examined_subsurfaces = []
        self.get_subsurfaces()

        for subsurface in self.subsurfaces:
            if self.is_examined_subsurface(subsurface):
                continue

            self.surface =  self.epcase.idf.newidfobject("AirflowNetwork:MultiZone:Surface".upper())
            self.surface.Surface_Name = subsurface.Name

            self.create_simple_opening(subsurface)
            self.surface.Leakage_Component_Name = self.opening.Name


    def create_simple_opening(self, subsurface):
        self.opening = self.epcase.idf.newidfobject("AirflowNetwork:MultiZone:Component:SimpleOpening".upper())
        self.opening.Name = f"{subsurface.Name} SimpleOpening"
        # taken from defaults 
        # https://bigladdersoftware.com/epx/docs/22-2/input-output-reference/group-airflow-network.html#airflownetworkmultizonecomponentsimpleopening
        self.opening.Discharge_Coefficient = 1
        self.opening.Air_Mass_Flow_Coefficient_When_Opening_is_Closed = 0.001
        self.opening.Minimum_Density_Difference_for_TwoWay_Flow = 0.0001
        

            
    def is_examined_subsurface(self, subsurface):
        try:  # only count interzones once...
            if subsurface.Outside_Boundary_Condition_Object in self.examined_subsurfaces:
                print(f"skipping {subsurface.Name}")
                return True
        except:
            pass # not an interzone object.. 
    
        self.examined_subsurfaces.append(subsurface.Name)
        return False


    def get_subsurfaces(self):
        g = Getter(self.epcase)
        g.get_subsurfaces()
        self.subsurfaces = g.subsurfaces
    