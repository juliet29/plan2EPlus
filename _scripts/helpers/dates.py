from datetime import date
from pathlib import Path


today = date.today().strftime("%y%m%d")




def create_save_details(case_name):
    FOLDER  = f"{today}_{case_name}"
    path = Path.cwd() / "figures" / FOLDER
    if not path.exists():
        path.mkdir()
    return path