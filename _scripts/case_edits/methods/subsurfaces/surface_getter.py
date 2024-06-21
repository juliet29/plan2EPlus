from case_edits.methods.subsurfaces.inputs import SurfaceGetterInputs


class SurfaceGetter():
    def __init__(self, inputs:SurfaceGetterInputs) -> None:
        self.inputs = inputs
        self.run()

    def run(self):
        self.update_curr_zones()
        self.find_surface()

    def update_curr_zones(self):
        self.curr_pair =  self.inputs.ssurface_pair
        self.curr_zone = self.get_zone(self.curr_pair[0])
        self.nb_zone = self.get_zone(self.curr_pair[1])

    def find_surface(self):
        for name, wall in self.curr_zone.walls.items():
            if wall.data.Outside_Boundary_Condition == "surface":
                if self.nb_zone.name in wall.data.Outside_Boundary_Condition_Object:
                    self.partner_surface = self.curr_zone.walls[wall.bunch_name]
                    return




    def get_zone(self, zone_num:int):
        zone_names = list(self.inputs.zones.keys())
        candidates = list(filter(lambda x: self.test_zone_name(x, zone_num), zone_names))
        assert len(candidates) == 1, f"Zones != 1: {candidates}"
        return self.inputs.zones[candidates[0]]


    def test_zone_name(self, zone_name:str, zone_num:int):
        test_name = f"0{zone_num}"
        if  test_name in zone_name:
            return True
        else:
            return False