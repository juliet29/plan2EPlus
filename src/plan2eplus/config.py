import pyprojroot
from pathlib import Path

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))


ENERGY_PLUS_LOCATION = Path.home().parent.parent / "Applications/EnergyPlus-22-2-0"
IDD_PATH = ENERGY_PLUS_LOCATION / "Energy+.idd"
IDF_PATH = BASE_PATH / "cases/base/01example/Minimal_AP.idf"
WEATHER_FILE = BASE_PATH / "weather_data/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"
