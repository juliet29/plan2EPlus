from __future__ import annotations

import case_edits.epcase as epcase
from helpers.ep_getter import Getter


class AirflowNetwork:
    def __init__(self, epcase: epcase.EneryPlusCaseEditor) -> None:
        self.epcase = epcase
        self.run()

    def run(self):
        self.create_simulation_control()
        self.find_afn_zones()
        self.create_zone_objects()
        self.create_zone_surfaces()
        self.get_afn_objects()
        # self.fix_no_vent()

    def create_simulation_control(self):
        self.sim_control = self.epcase.idf.newidfobject(
            "AirflowNetwork:SimulationControl".upper()
        )
        self.sim_control.Name = "AFN_SIM_CONTROL"
        self.sim_control.AirflowNetwork_Control = "MultizoneWithoutDistribution"

    def find_afn_zones(self):
        self.zones_w_subsurfaces = []
        for s in self.epcase.geometry.subsurfaces.values():
            self.zones_w_subsurfaces.append(s.wall.zone)

        self.zones_w_subsurfaces = set(self.zones_w_subsurfaces)

        # self.no_vent_zones = list(set(self.epcase.geometry.zone_list).difference(set(self.zones_w_subsurfaces)))

        # zone_objects = self.epcase.idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]
        # for zone in self.no_vent_zones:
        #     for obj in zone_objects:
        #         if obj.Zone_Name == zone.name:
        #             obj.Ventilation_Control_Mode = "NoVent"

    def create_zone_objects(self):
        for thermal_zone in self.zones_w_subsurfaces:
            self.zone = self.epcase.idf.newidfobject(
                "AirflowNetwork:MultiZone:Zone".upper()
            )
            self.zone.Ventilation_Control_Mode = "Constant"
            self.zone.Zone_Name = thermal_zone.name

    def create_zone_surfaces(self):
        self.examined_subsurfaces = []
        self.get_subsurfaces()

        for subsurface in self.subsurfaces:
            self.afn_surface = self.epcase.idf.newidfobject(
                "AirflowNetwork:MultiZone:Surface".upper()
            )
            self.afn_surface.Surface_Name = subsurface.Name

            self.create_simple_opening(subsurface)
            self.afn_surface.Leakage_Component_Name = self.opening.Name

    def create_simple_opening(self, subsurface):
        self.opening = self.epcase.idf.newidfobject(
            "AirflowNetwork:MultiZone:Component:SimpleOpening".upper()
        )
        self.opening.Name = f"{subsurface.Name} SimpleOpening"
        # taken from defaults
        self.opening.Discharge_Coefficient = 1
        self.opening.Air_Mass_Flow_Coefficient_When_Opening_is_Closed = 0.001
        self.opening.Minimum_Density_Difference_for_TwoWay_Flow = 0.0001

    # def fix_no_vent(self):
    #     self.update_no_vent_zones()
    #     self.identify_no_vent_walls()
    #     self.create_no_vent_surface()



    # def identify_no_vent_walls(self):
    #     self.no_vent_walls = []

    #     for zone in self.no_vent_zones:
    #         used_directions = []
    #         for w in zone.walls.values():
    #             if not w.partner_wall_name:
    #                 print((w.display_name, w.partner_wall_name))
    #                 used_directions.append(w.direction)
    #                 self.no_vent_walls.append(w)

    #             if len(used_directions) >= 2:
    #                 break

    # def create_no_vent_surface(self):
    #     min_flow_rate = self.epcase.idf.newidfobject(
    #             "AirflowNetwork:MultiZone:SpecifiedFlowRate".upper()
    #         )
    #     min_flow_rate.Name = "MinFlowRate"
    #     min_flow_rate.Air_Flow_Value = 0.0001
        

    #     for subsurface in self.no_vent_walls:
    #         self.afn_surface = self.epcase.idf.newidfobject(
    #             "AirflowNetwork:MultiZone:Surface".upper()
    #         )
    #         self.afn_surface.Surface_Name = subsurface.name
    #         self.afn_surface.Leakage_Component_Name = min_flow_rate.Name






    def get_subsurfaces(self):
        g = Getter(self.epcase)
        self.subsurfaces = g.get_original_subsurfaces()

    def get_afn_objects(self):
        g = Getter(self.epcase)
        g.get_afn_objects()
        self.afn_objects = g.afn_objects
