from pathlib import Path
from geomeppy import IDF
from rich import print as rprint
from eppy.runner.run_functions import EnergyPlusRunError
from ladybug.analysisperiod import AnalysisPeriod
import logging
from plan2eplus.graphbem.constants import (
    OUTPUT_BASE_PATH,
    WEATHER_PATH,
    graphbem_additional_variables_fx,
)
from plan2eplus.graphbem.study import create_graphbem_case
from plan2eplus.helpers.helpers import get_or_mkdir

logger = logging.getLogger(__name__)


def prep_cali_case(EPW_PATH: Path):
    assert EPW_PATH.suffix == ".epw"
    output_path = get_or_mkdir(OUTPUT_BASE_PATH / EPW_PATH.stem)
    analysis_period = AnalysisPeriod(st_month=8, end_month=8)
    get_additional_variables = graphbem_additional_variables_fx()
    return create_graphbem_case(
        output_path, EPW_PATH, analysis_period, get_additional_variables
    )


# get epw for each folder
def get_epws_for_graphbem():
    return list(WEATHER_PATH.rglob("*.epw"))


def run_cali_cases():
    epws = get_epws_for_graphbem()
    cases = [prep_cali_case(epw) for epw in epws]
    for case in cases:
        try:
            case.run_idf(force_run=True)
        except EnergyPlusRunError:
            rprint(f"[red bold] FAILED TO COMPLETE RUN FOR {case.path}")
            raise Exception

    # # logger.info(subdirectories)
    # rprint(subdirectories)


if __name__ == "__main__":
    # run_cali_cases()
    pass
