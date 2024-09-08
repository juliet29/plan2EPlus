from __future__ import annotations # TODO fix this!

import case_edits.epcase as epcase
from helpers.ep_getter import Getter
from collections import Counter

from collections import namedtuple

SubsurfaceZones = namedtuple("SubsurfaceZones", ["subsurface", "zone", "partner_zone"])


MIN_N_SUBSURFACES = 2

class AirflowNetwork:
    def __init__(self, epcase: epcase.EneryPlusCaseEditor) -> None:
        self.epcase = epcase
        self.run()

    def run(self):
        self.create_simulation_control()
        self.get_eligible_zones()
        self.create_zone_objects()
        self.get_eligible_subsurfaces()
        self.create_zone_surfaces()
        self.get_afn_objects()
        # self.fix_no_vent()

    def create_simulation_control(self):
        self.sim_control = self.epcase.idf.newidfobject(
            "AirflowNetwork:SimulationControl".upper()
        )
        self.sim_control.Name = "AFN_SIM_CONTROL"
        self.sim_control.AirflowNetwork_Control = "MultizoneWithoutDistribution"

  
    def get_eligible_zones(self):
        self.subsurface_zones: list[SubsurfaceZones] = []
        self.cnt = Counter()
        for k, v in self.epcase.geometry.subsurfaces.items():
            zone  = v.wall.zone
            self.cnt[zone]+=1
            p_zone = None
            if "Door" in k:
                p_zone, _ = self.get_partner_zone(v.name)
                self.cnt[p_zone]+=1
            s = SubsurfaceZones(v, zone, p_zone)
            self.subsurface_zones.append(s)

        self.eligible_zones = [k for k,v in self.cnt.items() if v >= MIN_N_SUBSURFACES]


    def create_zone_objects(self):
        for thermal_zone in self.eligible_zones:
            self.zone = self.epcase.idf.newidfobject(
                "AirflowNetwork:MultiZone:Zone".upper()
            )
            self.zone.Ventilation_Control_Mode = "Constant"
            self.zone.Zone_Name = thermal_zone.name

    def get_eligible_subsurfaces(self):
        ineligible_zones = [k for k,v in self.cnt.items() if v < 2]
        self.ineligible_surfaces = []
        for s  in self.subsurface_zones:
            if s.zone in ineligible_zones or s.partner_zone in ineligible_zones:
                self.ineligible_surfaces.append(s.subsurface.name)

    def create_zone_surfaces(self):
        self.get_subsurfaces()
        for subsurface in self.subsurfaces:
            if subsurface.Name not in self.ineligible_surfaces:
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


    def get_subsurfaces(self):
        g = Getter(self.epcase)
        self.subsurfaces = g.get_original_subsurfaces()

    def get_afn_objects(self):
        g = Getter(self.epcase)
        g.get_afn_objects()
        self.afn_objects = g.afn_objects


    
    def get_partner_zone(self, interzone_door_name):
        door_obj = self.epcase.idf.getobject("DOOR:INTERZONE", interzone_door_name)
        assert door_obj
        partner = door_obj["Outside_Boundary_Condition_Object"]
        partner_obj = self.epcase.idf.getobject("DOOR:INTERZONE", partner)
        assert partner_obj
        partner_wall = partner_obj["Building_Surface_Name"]

        [wall] =[w for w in self.epcase.geometry.walls.values() if w.name == partner_wall]

        return wall.zone, partner_wall



