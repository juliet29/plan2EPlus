from outputs.sql import SQLReader

class Plotter(SQLReader):
    def __init__(self, CASE_NAME) -> None:
        super().__init__(CASE_NAME)

    def set_color_schemes(self, color_scheme):
        self.color_scheme = color_scheme

    def check_dataset_is_zonal(self, dataset_name):
        if "zone" not in dataset_name:
            raise Exception(f"Dataset `{dataset_name}` is not zonal!")
        
    def check_dataset_is_surface(self, dataset_name):
        if "surf" not in dataset_name:
            raise Exception(f"Dataset `{dataset_name}` is not for surfaces!")
        
    