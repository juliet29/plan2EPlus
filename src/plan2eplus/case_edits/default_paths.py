from pathlib import Path
from plan2eplus.paths import path_class

# external paths
ENERGY_PLUS_LOCATION = Path.home().parent.parent / "Applications/EnergyPlus-22-2-0"
DEFAULT_IDD = (
    ENERGY_PLUS_LOCATION / "Energy+.idd"
)  # TODO this is something that people have to specify on their own laptop..

DEFAULT_IDF = path_class.inputs / "base/01example/Minimal_AP.idf"

WEATHER_FILE = path_class.inputs / "weather/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"
