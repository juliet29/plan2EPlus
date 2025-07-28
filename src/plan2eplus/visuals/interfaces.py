from dataclasses import dataclass
from pathlib import Path

from eppy.bunch_subclass import EpBunch
from geomeppy import IDF
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from rich import print as rprint

from plan2eplus.geometry.directions import WallNormal
from plan2eplus.geometry.domain import Domain, MultiDomain
from plan2eplus.helpers.ep_constants import (
    DOOR,
    FLOOR,
    OUTDOORS,
    ROOF,
    WALL,
    BUILDING_SURFACE,
    ZONE,
)
from plan2eplus.helpers.ep_helpers import get_zones
from plan2eplus.geometry.range import (
    Range,
)
from plan2eplus.helpers.helpers import chain_flatten, sort_and_group_objects_dict
from plan2eplus.geometry.coords import Coord
from plan2eplus.visuals.idf_name import decompose_idf_name
from plan2eplus.visuals.projections import (
    compute_unit_normal,
    get_surface_domain,
    get_position_along_normal_axis,
)
from typing import NamedTuple
from plan2eplus.custom_exceptions import PlanMismatchException


def get_idfobject_by_name_and_key(idf: IDF, key: str, name: str):
    return idf.getobject(key.upper(), name)


def get_idfobject_key(ep_object: EpBunch):
    return ep_object.obj[0]


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
    construction: str | None = None

    @property
    def unit_normal_drn(self):
        return compute_unit_normal(self.ep_object)

    @property
    def domain(self):
        return get_surface_domain(self.ep_object, self.unit_normal_drn)

    @property
    def linear_component(self):  # TODO include a direction..
        return self.domain.horz_range

    @property
    def centroid(self):  # TODO include a direction..
        other_pos = get_position_along_normal_axis(self.ep_object, self.unit_normal_drn)
        # rprint(f"other pos: {other_pos}")
        if self.unit_normal_drn == "X":
            return Coord(other_pos, self.linear_component.midpoint)
        elif self.unit_normal_drn == "Y":
            return Coord(
                self.linear_component.midpoint,
                other_pos,
            )
        else:
            raise NotImplementedError("only considered x + y!")

    def assign_construction(self, construction_name: str):
        # rprint(f"my const will be - {construction_name}")
        self.construction = construction_name  # TODO does this not persist?
        # TODO IDF assigns in outer function..

    def update_construction_on_idf(self):
        assert self.construction
        # rprint(f"my const is - {self.construction}")
        self.ep_object.Construction_Name = self.construction


@dataclass
class Subsurface(LinearGeometryObject):
    @property
    def nickname(self):
        return f"{self.dname.object_type}-B{self.dname.zone_number}-{self.dname.surface_type}-{self.dname.direction_number}-{self.dname.position_number}"

    @property
    def is_door(self):
        return (
            get_idfobject_key(self.ep_object) == DOOR or self.dname.object_type == DOOR
        )  # TODO better way to figure out the object type..

    def __repr__(self) -> str:
        return f"{self.nickname}"


@dataclass
class Surface(LinearGeometryObject):
    @classmethod
    def create(cls, idf: IDF, idf_name: str):
        object = idf.getobject(BUILDING_SURFACE, idf_name)
        assert object, "Invalid surface name"
        return cls(object)

    # TODO class method -> idf + object name to create -> everything that inherits has to implement.. ? or put it directly on the objects

    # TODO interior, partners..
    @property
    def direction(self):
        if self.is_wall:
            rounded_azimuuth = round(float(self.ep_object.azimuth))
            return WallNormal(rounded_azimuuth)
        elif self.is_floor:
            return WallNormal.DOWN
        elif self.is_roof:
            return WallNormal.UP
        else:
            raise NotImplementedError(
                "Haven't implemented direction for this type of surface!"
            )

    @property
    def nickname(self):
        return f"{self.dname.surface_type}`B{self.dname.zone_number}-{self.dname.plan_name_alone}`-{self.direction.name}({self.dname.direction_number})-{self.dname.position_number}"

    @property
    def subsurfaces(self):
        return [Subsurface(obj) for obj in self.ep_object.subsurfaces]  # type: ignore # TODO eppy type issue

    # TOOD CAN add to extended geom object .., only need at certain point..
    @property
    def is_interior(self):
        return self.ep_object.Outside_Boundary_Condition.lower() != OUTDOORS

    @property
    def is_wall(self):
        return self.ep_object.Surface_Type.lower() == WALL

    @property
    def is_floor(self):
        return self.ep_object.Surface_Type.lower() == FLOOR

    @property
    def is_roof(self):
        return self.ep_object.Surface_Type.lower() == ROOF

    @property
    def is_ceiling(self):
        return self.ep_object.Surface_Type.lower() == ROOF and self.is_interior

    def partner_wall(self, idf: IDF):
        if self.is_interior and self.is_wall:
            # rprint(f"Im an inside wall {self.nickname} - and my partner is {self.ep_object.Outside_Boundary_Condition_Object}")
            partner_wall = self.ep_object.Outside_Boundary_Condition_Object
            assert partner_wall
            partner_wall_object = get_idfobject_by_name_and_key(
                idf, get_idfobject_key(self.ep_object), partner_wall
            )
            assert partner_wall_object
            return Surface(partner_wall_object)
        else:
            return None  # TODO OR reais exception??

    def __repr__(self) -> str:
        return f"{self.nickname}"


class ZoneDirectedWalls(NamedTuple):
    NORTH: list[Surface]
    EAST: list[Surface]
    SOUTH: list[Surface]
    WEST: list[Surface]

    def __getitem__(self, i):
        return getattr(self, i)


@dataclass
class Zone(GeometryObject):
    @classmethod
    def create(cls, idf: IDF, idf_name: str):
        object = idf.getobject(ZONE, idf_name)
        assert object, "Invalid zone name"
        return cls(object)

    @property
    def nickname(self):
        return f"B{self.dname.zone_number}"

    @property
    def surfaces(self):
        return [Surface(obj) for obj in self.ep_object.zonesurfaces]  # type: ignore # TODO eppy type issue

    @property
    def walls(self):
        return [s for s in self.surfaces if s.is_wall]

    @property
    def interior_walls(self):
        return [s for s in self.surfaces if s.is_interior and s.is_wall]

    @property
    def directed_walls(self):
        res = sort_and_group_objects_dict(self.walls, lambda s: s.direction)

        # rprint(res)
        # rprint(type(res))
        return ZoneDirectedWalls(*[i for i in res.values()])

    @property
    def subsurfaces(self):
        return chain_flatten([s.subsurfaces for s in self.surfaces if s.subsurfaces])

    @property
    def domain(self):
        floor = [s for s in self.surfaces if s.dname.surface_type == "Floor"]
        assert len(floor) == 1, rprint(f"Invalid floor for zone  -> {floor}")
        return get_surface_domain(floor[0].ep_object, "Z")

    # # TODO all plotting stuff extends the object and goes in a different file
    # def plot_zone_midpoints(self, ax: Axes | None = None):
    #     if not ax:
    #         _, ax = plt.subplots()
    #     x, y = zip(*self.domain.perimeter_midpoints.as_pairs)
    #     ax.scatter(x, y)  # dont just want midpoints, actually want the walls..

    def plot_zone_name(self, ax: Axes | None = None):
        if not ax:
            _, ax = plt.subplots()
        ax.text(
            *self.domain.centroid,
            s=f"{self.nickname}-{self.dname.plan_name}",
            fontsize="x-small",
        )

    def __repr__(self) -> str:
        return f"{self.nickname}"


# def get_zones(idf: IDF) -> list[EpBunch]:
#     return [i for i in idf.idfobjects["ZONE"]]


# class PlanExternalPositions(NamedTuple):
#     NORTH: Coord
#     EAST: Coord
#     SOUTH: Coord
#     WEST: Coord

#     def __getitem__(self, i):
#         return getattr(self, i)


@dataclass
class PlanZones:  # can just call Plan..
    idf: IDF

    @property
    def zones(self):
        return [
            Zone(obj) for obj in get_zones(self.idf)
        ]  # TODO replace with ephelpers?

    @property
    def zone_dict(self):
        return {z.nickname: z for z in self.zones}

    @property
    def domains(self):
        return MultiDomain([i.domain for i in self.zones])

    @property
    def surfaces_and_subsurfaces(self):
        surfaces = chain_flatten([z.surfaces for z in self.zones])
        subsurfaces = chain_flatten([z.subsurfaces for z in self.zones])
        return surfaces + subsurfaces

    def get_zone_by_num(self, num: int):
        for v in self.zones:
            if v.dname.zone_number == num:
                return v
        raise PlanMismatchException("Invalid zone number")

    def get_zone_by_plan_name(self, plan_name: str):
        for v in self.zones:
            if v.dname.plan_name_alone == plan_name:
                return v
        raise PlanMismatchException(f"Name: {plan_name} is not valid")

    # TODO all plotting stuff extends the object and goes in a different file
    def plot_zone_domains(self, ax: Axes | None = None):
        if not ax:
            _, ax = plt.subplots()
        xlim, ylim = self.domains.extents

        for d in self.domains.domains:
            ax.add_artist(d.get_mpl_patch())

        ax.set(xlim=xlim, ylim=ylim)
        for zone in self.zones:
            zone.plot_zone_name(ax)

        plt.show()

        return ax
