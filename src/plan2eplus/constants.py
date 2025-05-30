import pyprojroot
from pathlib import Path


ENERGY_PLUS_LOCATION = Path.home().parent.parent / "Applications/EnergyPlus-22-2-0"
IDD_PATH = ENERGY_PLUS_LOCATION / "Energy+.idd"


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
IDF_PATH = BASE_PATH / "cases/base/01example/Minimal_AP.idf"
WEATHER_FILE = BASE_PATH.parent / "weather_data/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"


PATH_TO_OUTPUT_CASES = BASE_PATH / "cases"
# TODO for extensibility, this gets copied over to this directory...

DUMMY_OUTPUT_PATH = PATH_TO_OUTPUT_CASES / "tests/dummy"



# however SVG2Plan will eventually become a sub-module so will have to deal with in a more sophisticated wau
PATH_TO_SVG2PLAN_CASES = (
    BASE_PATH.parent / "svg2plan/outputs2/"
)  # think this should be a vairable no? -> CURRENTLY "svg2plan/svg2plan_outputs_p1gen"


PATH_TO_GRAPH2PLAN_CASES = (
    BASE_PATH.parent / "graph2plan/outputs"
) 


SRC_PATH = BASE_PATH / "src/plan2eplus"