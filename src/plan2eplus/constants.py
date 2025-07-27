import pyprojroot
from pathlib import Path

# rename to be paths


ENERGY_PLUS_LOCATION = Path.home().parent.parent / "Applications/EnergyPlus-22-2-0"
IDD_PATH = ENERGY_PLUS_LOCATION / "Energy+.idd"# TODO this is something that people have to specify on their own laptop.. 


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))

CONFIG_DIR = BASE_PATH / "config"
LOG_DIR = BASE_PATH / "logs"


IDF_PATH = BASE_PATH / "cases/base/01example/Minimal_AP.idf"
WEATHER_FILE = BASE_PATH.parent / "weather_data/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"


PATH_TO_OUTPUT_CASES = BASE_PATH / "cases"
# TODO for extensibility, this gets copied over to this directory...

PATH_TO_DUMMY_OUTPUTS = PATH_TO_OUTPUT_CASES / "tests/dummy"
PATH_TO_GRAPHBEM_OUTPUTS = (
    PATH_TO_OUTPUT_CASES / "tests/graphbem"
)  # TODO put in a local interfaces.py
PATH_TO_GRAPHBEM_INPUTS = BASE_PATH.parent / "graphBEM"


# however SVG2Plan will eventually become a sub-module so will have to deal with in a more sophisticated wau
PATH_TO_SVG2PLAN_CASES = (
    BASE_PATH.parent / "svg2plan/outputs2/"
)  # think this should be a vairable no? -> CURRENTLY "svg2plan/svg2plan_outputs_p1gen"


PATH_TO_GRAPH2PLAN_CASES = BASE_PATH.parent / "graph2plan/outputs"


SRC_PATH = BASE_PATH / "src/plan2eplus"

MATERIALS_PATH = BASE_PATH / "cases/constructions"


# -------
DEFAULT_IDF_NAME = "out.idf"
DEFAULT_SQL_NAME = "eplusout.sql"
DEFAULT_SQL_SUBPATH = f"results/{DEFAULT_SQL_NAME}"
