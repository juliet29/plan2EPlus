from methods.subsurfaces.inputs import SurfaceGetterInputs
from geometry.wall import WallNormal



class SurfaceGetter:
    """Automatially gets surfaces based on zones that are being connected, or direction cbeing connected to.. """
    def __init__(self, inputs: SurfaceGetterInputs) -> None:
        self.inputs = inputs
        self.curr_pair = self.inputs.ssurface_pair
        self.zone_names = list(self.inputs.zones.keys())
        self.run()

    def run(self):
        self.curr_zone = self.get_zone(self.curr_pair[0])
        if type(self.curr_pair[1]) == WallNormal:
            self.dir = self.curr_pair[1]
            self.find_surface_by_direction()
        elif type(self.curr_pair[1]) == int:
            self.nb_zone = self.get_zone(self.curr_pair[1])
            self.find_surface_by_partner()

    def find_surface_by_direction(self):
        self.dir = self.curr_pair[1]
        candidates = [w for w in self.curr_zone.walls.values() if w.direction == self.dir.name] #type:ignore
        self.check_if_unique(candidates)
        self.goal_surface = candidates[0]

    def find_surface_by_partner(self):
        for name, wall in self.curr_zone.walls.items():
            if wall.data.Outside_Boundary_Condition == "surface":
                if self.nb_zone.name in wall.data.Outside_Boundary_Condition_Object:
                    self.goal_surface = self.curr_zone.walls[wall.bunch_name]
                    return

    def get_zone(self, zone_num: int):
        candidates = list(
            filter(lambda x: self.test_zone_name(x, zone_num), self.zone_names)
        )
        self.check_if_unique(candidates)
        return self.inputs.zones[candidates[0]]

    def test_zone_name(self, zone_name: str, zone_num: int):
        test_name = f"0{zone_num}"
        if test_name in zone_name:
            return True
        else:
            return False

    def check_if_unique(self, candidates):
        assert len(candidates) == 1, f"Zones != 1: {candidates}"
