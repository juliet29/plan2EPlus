from pathlib import Path
from geomeppy import IDF
from plan2eplus.constants import PATH_TO_GRAPHBEM_INPUTS
from rich import print as rprint
import logging

GRAPHBEM_WEATHER_PATH = PATH_TO_GRAPHBEM_INPUTS / "energyPlus/weather/CAClimateZones/"

logger = logging.getLogger(__name__)


def prep_cali_case(epw: Path):
    pass


# get epw for each folder
def get_epws_for_graphbem():
    subdirectories = [item for item in GRAPHBEM_WEATHER_PATH.iterdir() if item.is_dir()]

    # logger.info(subdirectories)
    rprint(subdirectories)


if __name__ == "__main__":
    # logger.info("Starting august study")
    get_epws_for_graphbem()
