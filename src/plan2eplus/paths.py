import pyprojroot
from pathlib import Path
from utils4plans.paths import StaticPaths
from dataclasses import dataclass

# rename to be paths




BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
path_class = StaticPaths("", base_path=BASE_PATH)




# relative paths -> think this stuff is better defined locally.. 


# other.. 
CONFIG_DIR = BASE_PATH / "config"
LOG_DIR = BASE_PATH / "logs"






PATH_TO_OUTPUT_CASES = path_class.models
# TODO for extensibility, this gets copied over to this directory...

PATH_TO_DUMMY_OUTPUTS = PATH_TO_OUTPUT_CASES / "tests/dummy"



# however SVG2Plan will eventually become a sub-module so will have to deal with in a more sophisticated wau
PATH_TO_SVG2PLAN_CASES = (
    BASE_PATH.parent / "svg2plan/outputs2/"
)  # think this should be a vairable no? -> CURRENTLY "svg2plan/svg2plan_outputs_p1gen"


PATH_TO_GRAPH2PLAN_CASES = BASE_PATH.parent / "graph2plan/outputs"


SRC_PATH = BASE_PATH / "src/plan2eplus"

MATERIALS_PATH = BASE_PATH / "cases/constructions"


# ------- # TODO => move to constants.. 
DEFAULT_IDF_NAME = "out.idf"
DEFAULT_SQL_NAME = "eplusout.sql"
DEFAULT_SQL_SUBPATH = f"results/{DEFAULT_SQL_NAME}"
