from case_edits.epcase import EneryPlusCaseEditor
from case_edits.ezcase import EzCase

class SurfaceGetter():
    def __init__(self, ezcase:EzCase) -> None:
        self.ezcase = ezcase
        self.curr_pair = ezcase.door_pairs[0]

        self.run()

    def run(self):
        self.update_curr_zones()
        self.find_surface()

    def update_curr_zones(self):
        self.curr_zone = self.get_zone(self.curr_pair[0])
        self.nb_zone = self.get_zone(self.curr_pair[1])

    def find_surface(self):
        for name, wall in self.curr_zone.walls.items():
            if wall.data.Outside_Boundary_Condition == "surface":
                print(wall.name)
                if self.nb_zone.name in wall.name:
                    print(wall)



    def get_zone(self, zone_num:int):
        zone_names = list(self.ezcase.zones.keys())
        candidates = list(filter(lambda x: self.test_zone_name(x, zone_num), zone_names))
        assert len(candidates) == 1, f"Zones != 1: {candidates}"
        return self.ezcase.zones[candidates[0]]


    def test_zone_name(self, zone_name:str, zone_num:int):
        test_name = f"0{zone_num}"
        if  test_name in zone_name:
            return True
        else:
            return False