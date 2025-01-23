from pathlib import Path

from eppy.runner.run_functions import EnergyPlusRunError
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.epw import EPW

from ...case_edits.epcase import EneryPlusCaseEditor
from ...case_edits.ezcase import create_ezcase
from ..experiments.dynamic_door_sched import (
    add_dynamic_vent_sched_to_doors,
    close_doors,
)
from ...helpers.dates import today
from ...plan.interfaces import WindowChangeData
from ..setup.setup import get_case_names

EXP_GROUP = f"{today}_summer"
RUN_CONTROL = False
epw_path = Path.cwd() / "weather_data" / "USA_CA_Palo.Alto.AP.724937_TMYx.epw"
epw = EPW(epw_path)
ap = AnalysisPeriod(st_month=6, end_month=10, timestep=4)

exp_groups = {
    "yesterday_one_day": "241119",
    "today_summer": "241120_summer"
}

def get_input_dir(input_case_name):
    return f"case_{input_case_name}"


def create_dirs(output_folder, input_case_name, ctype):
    output_case_name = f"{input_case_name}_{ctype}"
    output_dir = f"{EXP_GROUP}_{output_folder}/{output_case_name}"
    input_dir = get_input_dir(input_case_name)
    return output_dir, input_dir, output_case_name


def run_case(ezcase: EneryPlusCaseEditor, output_case_name="", run_control=RUN_CONTROL, ): 
    if run_control:
        try:
            ezcase.run_idf(force_run=True)
        except EnergyPlusRunError:
            raise Exception(f"------{output_case_name.upper()} FAILED!!!!!---")


def compare_materials(input_case_name):
    def create_cases(ctype):
        output_dir, input_dir, output_case_name = create_dirs(output_folder, input_case_name, ctype)
        ezcase = create_ezcase(
            output_dir, input_dir, cons_set_type=ctype, epw=epw, analysis_period=ap
        )
        run_case(ezcase, output_case_name)
        return

    output_folder = "materials"
    ctypes = ["Light", "Medium", "Heavy"]
    for ctype in ctypes:
        create_cases(ctype)


def compare_door_schedule(input_case_name):
    def create_cases(ctype):
        output_dir, input_dir, output_case_name = create_dirs(output_folder, input_case_name, ctype)

        ezcase = create_ezcase(output_dir, input_dir, epw=epw, analysis_period=ap)
        match ctype:
            case "CLOSED":
                ezcase.idf = close_doors(ezcase.idf)
            case "DYNAMIC":
                ezcase.idf = add_dynamic_vent_sched_to_doors(
                    ezcase.idf, ezcase.idf_path
                )
        run_case(ezcase, output_case_name)

    output_folder = "doors"
    ctypes = ["CLOSED", "DYNAMIC"]
    for ctype in ctypes:
        create_cases(ctype)


def compare_window_size(input_case_name):
    def create_cases(ctype):
        output_dir, input_dir, output_case_name = create_dirs(output_folder, input_case_name, ctype)
        ezcase = create_ezcase(
            output_dir,
            input_dir,
            win_change_data=WindowChangeData(True, ctype),
            epw=epw,
            analysis_period=ap,
        )
        run_case(ezcase, output_case_name)

    output_folder = "windows"
    ctypes = [1.3, 0.7]
    for ctype in ctypes:
        create_cases(ctype)


def execute_experiment():
    for input_case_name in get_case_names():
        compare_materials(input_case_name)
        compare_window_size(input_case_name)
        compare_door_schedule(input_case_name)





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
