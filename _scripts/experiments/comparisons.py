from itertools import product
from constructions.constructions import CONSTRUCTION_SET_TYPE
from plan.interfaces import WindowChangeData
from setup.setup import get_case_names
from case_edits.ezcase import create_ezcase
from dynamic_door_sched import add_dynamic_vent_sched_to_doors, close_doors


# materials 9 cases
# materials setup.. '

# def create_dirs(comparison_type, comparison_names):
#     case_names = get_case_names()
#     input_dirs = [f"case_{i}" for i in case_names]
#     output_combos = list(product(comparison_names, input_dirs))
#     output_case_names = [f"{c}_{i}" for c, i in output_combos]
#     output_dirs = [f"{comparison_type}/{m}" for m in output_case_names]

def get_input_dir(input_case_name):
    return f"case_{input_case_name}"

def create_dirs(output_folder, input_case_name, ctype):
        output_case_name = f"{input_case_name}_{ctype}"
        output_dir = f"{output_folder}/{output_case_name}"
        input_dir = get_input_dir(input_case_name)
        return output_dir, input_dir

def compare_materials(input_case_name):
    def create_cases(ctype: CONSTRUCTION_SET_TYPE):
        output_dir, input_dir = create_dirs(output_folder, input_case_name, ctype)
        ezcase = create_ezcase(output_dir, input_dir, cons_set_type=ctype)
        # run case 
        return 

    output_folder = "materials"
    ctypes = ['Light', 'Medium', 'Heavy']


def compare_door_schedule(input_case_name):
    def create_cases(ctype):
        output_dir, input_dir = create_dirs(output_folder, input_case_name, ctype)

        match ctype:
            case "CLOSED":
                ezcase = create_ezcase(output_dir, input_dir)
                ezcase.idf = close_doors(ezcase.idf)
            case "DYNAMIC":
                ezcase = create_ezcase(output_dir, input_dir)
                ezcase.idf = add_dynamic_vent_sched_to_doors(ezcase.idf, ezcase.idf_path)
            case _:
                raise Exception("Invalid case")
        
    output_folder="doors"
    ctypes = ["CLOSED", "DYNAMIC"]

def compare_window_size(input_case_name):
    def create_cases(ctype):
        output_dir, input_dir = create_dirs(output_folder, input_case_name, ctype)
        ezcase = create_ezcase(output_dir, input_dir, win_change_data=WindowChangeData(True, ctype))

        
    output_folder="windows"
    ctypes = [1.3, 0.7]






# can pass area factor though ezcase.. , 6 cases
# subsurface_attrs = load_attributes(case.path_to_input)
# window_dims.modify_area(0.9).area / window_dims.area


# close doors, 3 cases
# doors = [i for i in  case2.idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"] if "Door" in i.Surface_Name ]

# for door in doors:
#     door.Ventilation_Control_Mode = "NoVent"



# variable door schedule, 3 cases..




# weather => summer...,find TMY files..
    # ap = AnalysisPeriod(st_month=6, end_month=10, timestep=INTERVALS_PER_HOUR)




