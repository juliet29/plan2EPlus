from methods.subsurfaces.inputs import SurfaceGetterInputs
from geometry.wall_normal import WallNormal
from helpers.idf_object_rename import convert_block_name_to_int


class SurfaceGetter:
    """Automatially gets surfaces based on zones that are being connected, or direction cbeing connected to.."""

    def __init__(self, inputs: SurfaceGetterInputs) -> None:
        self.space_a, self.space_b = (
            inputs.ssurface_pair.space_a,
            inputs.ssurface_pair.space_b,
        )
        self.zones = inputs.zones
        self.zone_names = list(self.zones.keys())
        self.run()

    def run(self):
        self.curr_zone = self.get_zone(self.space_a)
        if type(self.space_b) == WallNormal:
            self.dir = self.space_b
            self.find_surface_by_direction()
        elif type(self.space_b) == int:
            self.nb_zone = self.get_zone(self.space_b)
            self.find_surface_by_partner()

    def find_surface_by_direction(self):
        self.dir = self.space_b
        candidates = [
            w for w in self.curr_zone.walls.values() if w.direction == self.dir.name
        ]  # type:ignore
        # TODO handle if a zone has multiple walls shared with a partner, or multiple walls in one direction
        self.is_unique_block(candidates)
        self.goal_surface = candidates[0]

    def find_surface_by_partner(self):
        for wall in self.curr_zone.walls.values():
            if wall.data.Outside_Boundary_Condition == "surface":
                if self.nb_zone.name in wall.data.Outside_Boundary_Condition_Object:
                    self.goal_surface = self.curr_zone.walls[wall.bunch_name]
                    return

    def get_zone(self, zone_num: int):
        candidates = list(
            filter(lambda x: self.test_zone_name(x, zone_num), self.zone_names)
        )
        try:
            self.is_unique_block(candidates)
        except:
            print(f"trying for {zone_num}")
            raise Exception(f"candidates = {candidates}")
        return self.zones[candidates[0]]

    def test_zone_name(self, zone_name: str, zone_num: int):
        test_name = convert_block_name_to_int(zone_name)
        if test_name == zone_num:
            return True
        else:
            return False

    def is_unique_block(self, candidates):
        assert len(candidates) == 1, f"Walls != 1: {candidates}"

    
