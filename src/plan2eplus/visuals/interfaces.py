from dataclasses import dataclass

from geomeppy import IDF
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from plan2eplus.helpers.ep_helpers import get_zones
from plan2eplus.helpers.geometry_interfaces import Domain, Range, WallNormal
from eppy.bunch_subclass import EpBunch
from plan2eplus.helpers.ep_helpers import get_zone_num


from rich import print as rprint

from plan2eplus.helpers.helpers import chain_flatten
from plan2eplus.visuals.idf_name import decompose_idf_name
from plan2eplus.visuals.projections import compute_unit_normal, get_surface_domain


@dataclass
class GeometryObject:
    ep_object: EpBunch  # TODO make assertions about the shape of the object?

    @property
    def idf_name(self):
        return str(self.ep_object.Name)

    @property
    def dname(self):
        return decompose_idf_name(self.idf_name)


@dataclass
class LinearGeometryObject(GeometryObject):
    @property
    def unit_normal_drn(self):
        return compute_unit_normal(self.ep_object)

    @property
    def domain(self):
        return get_surface_domain(self.ep_object, self.unit_normal_drn)

    @property
    def linear_component(self):
        return self.domain.horz_range


@dataclass
class Zone(GeometryObject):
    @property
    def nickname(self):
        return f"B{self.dname.zone_number}"

    @property
    def surfaces(self):
        return [Surface(obj) for obj in self.ep_object.zonesurfaces]  # type: ignore # TODO eppy type issue

    @property
    def subsurfaces(self):
        return chain_flatten([s.subsurfaces for s in self.surfaces if s.subsurfaces])

    @property
    def domain(self):
        floor = [s for s in self.surfaces if s.dname.surface_type == "Floor"]
        assert len(floor) == 1
        return get_surface_domain(floor[0].ep_object, "Z")
    
    def plot_zone_midpoints(self, ax: Axes | None = None):
        if not ax:
            _, ax = plt.subplots()
        x,y = zip(*self.domain.perimeter_midpoints.as_pairs)
        ax.scatter(x,y)

    def __repr__(self) -> str:
        return f"{self.nickname}"


@dataclass
class Surface(LinearGeometryObject):
    # TODO interior, partners..
    @property
    def direction(self):
        rounded_azimuuth = round(float(self.ep_object.azimuth))
        return WallNormal(rounded_azimuuth)

    @property
    def nickname(self):
        return f"B{self.dname.zone_number}-{self.dname.surface_type}-{self.direction.name}({self.dname.direction_number})-{self.dname.position_number}"

    @property
    def subsurfaces(self):
        return [Subsurface(obj) for obj in self.ep_object.subsurfaces]  # type: ignore # TODO eppy type issue

    def __repr__(self) -> str:
        return f"{self.nickname}"


@dataclass
class Subsurface(LinearGeometryObject):
    surface: Surface | None = None

    # ideally get direction of wall its on..

    @property
    def nickname(self):
        return f"{self.dname.object_type}-B{self.dname.zone_number}-{self.dname.surface_type}-{self.dname.direction_number}-{self.dname.position_number}"

    def __repr__(self) -> str:
        return f"{self.nickname}"

    # surface: str
    # domain: Domain


@dataclass
class PlanZones: # can just call Plan.. 
    idf: IDF

    @property
    def zones(self):
        return [Zone(obj) for obj in get_zones(self.idf)]

    @property
    def zone_dict(self):
        return [Zone(obj) for obj in get_zones(self.idf)]
    
    @property 
    def domains(self):
        return [i.domain for i in self.zones]

    def get_zone_by_num(self, num: int):
        for v in self.zones:
            if v.dname.zone_number == num:
                return v
        raise Exception("Invalid zone number")
    
    def get_plan_extents(self, PAD_BASE=1.4):
        PAD = PAD_BASE * 1.1
        min_x = min([i.horz_range.min for i in self.domains]) - PAD
        max_x = max([i.horz_range.max for i in self.domains]) + PAD
        min_y = min([i.vert_range.min for i in self.domains]) - PAD
        max_y = max([i.vert_range.max for i in self.domains]) + PAD
        return (min_x, max_x), (min_y, max_y)
    
    # TODO more intense plotting things maybe go elsewhere?
    def plot_zone_domains(self, ax: Axes | None = None):
        if not ax:
            _, ax = plt.subplots()
        xlim, ylim = self.get_plan_extents()
        
        for d in self.domains:
            ax.add_artist(d.get_mpl_patch())
    
        ax.set(xlim=xlim, ylim=ylim)
        self.zones[0].plot_zone_midpoints(ax)

        plt.show()

    
        return ax
    
    
    

    


    # def get_zone_wall_on_facade(
    #     self, surfaces: dict[str, Surface], zone_num: int, drn: WallNormal
    # ):
    #     zone_surfaces = self.get_zone_surfaces(zone_num, surfaces)
    #     return [z for z in zone_surfaces if z.direction == drn]
    #     # TODO want to find the middle coordinate..


# @dataclass
# class Plan:
#     zones: dict[str, Zone]
#     surfaces: dict[str, Surface]
#     subsurfaces: dict[str, Subsurface]
#     # room_map: dict

#     def __post_init__(self):
#         for surface in self.surfaces.values():
#             surface.zone = self.zones[surface.ep_object.Zone_Name]

#         for subsurface in self.subsurfaces.values():
#             subsurface.surface = self.surfaces[
#                 subsurface.ep_object.Building_Surface_Name
#             ]
#         # for zone in self.zones.values():
#         #     potential_surfaces = []

#     @property
#     def domain(self):
#         pass  # created from Zones
#         # TODO refactor plot_helpers.get_domains_lim -> min, max here.. `plan2eplus/src/plan2eplus/studies/analysis/plot_helpers.py:17`

#     def __repr__(self) -> str:
#         z = f"zones: {[i.nickname for i in self.zones.values()]}\n"
#         s = f"surfaces: {[i.nickname for i in self.surfaces.values()]}\n"
#         ss = f"subsurfaces: {[i.nickname for i in self.subsurfaces.values()]}\n"
#         return z + s + ss

#     # now goes through and populates connections?
