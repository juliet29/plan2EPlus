from munch import Munch

class DynamicOutputVariables(Munch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_t1_var(self, qoi, space, increment):
        var = f"{space} {qoi} {increment}"
        class_name = qoi.lower().replace(" ", "_")
        self[class_name] = var

    def show_vars_to_add(self):
        for k,v in self.items():
            print(f"{k} = '{v}'")

    def show_keys(self):
        keys_list = []
        for k in self.keys():
            keys_list.append('ov.{k}')
        print(keys_list)


qois = ["Inside Face Convection Heat Gain",
	"Inside Face Net Surface Thermal Radiation Heat Gain",
	"Inside Face Solar Radiation Heat Gain",
	"Surface Inside Face Internal Gains Radiation"]

d = DynamicOutputVariables()
for qoi in qois:
    d.create_t1_var(qoi, "Zone", "Rate per Area")
d.show_keys()