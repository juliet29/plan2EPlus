import filecmp
import os
from pathlib import Path
from typing import Optional

from ..constants import IDD_PATH, IDF_PATH, DEFAULT_IDF_NAME

from ..constants import WEATHER_FILE
from eppy.runner.run_functions import EnergyPlusRunError
from geomeppy import IDF
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.epw import EPW
from rich import print as rprint
from typing import NamedTuple

IDF.setiddname(IDD_PATH)


def update_idf_location(idf: IDF, epw: EPW):
    loc = idf.newidfobject("SITE:LOCATION")
    loc.Name = epw.location.city
    loc.Latitude = epw.location.latitude
    loc.Longitude = epw.location.longitude
    loc.Time_Zone = epw.location.time_zone
    loc.Elevation = epw.location.elevation
    return idf


def update_idf_run_period(idf: IDF, ap: AnalysisPeriod):
    rp = idf.newidfobject("RUNPERIOD")
    rp.Name = "Summer"
    rp.Begin_Month = ap.st_month
    rp.End_Month = ap.end_month
    rp.Begin_Day_of_Month = ap.st_day
    rp.End_Day_of_Month = ap.end_day
    return idf


class EneryPlusCaseEditor:
    def __init__(
        self,  # TODO make inputs a  dataclalss..
        path_to_outputs: Optional[Path] = None,
        starting_path: Optional[Path] = None,
        epw: EPW | Path | None = None,  # todo should be path
        analysis_period: AnalysisPeriod | None = None,
    ) -> None:
        # TODO make this objects
        self.path = path_to_outputs
        self.starting_path = starting_path
        self.is_changed_idf = True
        self.is_failed_simulation = False
        self.analysis_period: AnalysisPeriod | None = analysis_period
        self.epw = epw

        self.get_idf()
        self.update_weather_and_run_period()

    def __repr__(self):
        return f"EPCaseEditor({self.path.name if self.path else ''})"

    def get_idf(self):
        if not self.starting_path:
            self.idf = IDF(IDF_PATH)
        else:
            self.idf = IDF(self.starting_path)

    def compare_and_save(self):
        if not self.path:
            raise Exception("Can't save, no output directory!")

        self.temp_idf_path = self.path / "temp.idf"
        self.idf_path = self.path / DEFAULT_IDF_NAME
        self.idf.save(filename=self.temp_idf_path)

        dir_files = list(self.path.iterdir())
        if DEFAULT_IDF_NAME in dir_files:
            print(f"{DEFAULT_IDF_NAME} exists")
            self.is_changed_idf = not filecmp.cmp(self.temp_idf_path, self.idf_path)
            print(f"IDF has changed: {self.is_changed_idf}")
        else:
            print("out.idf does not exist")
            self.is_changed_idf = True

        self.idf.save(filename=self.idf_path)
        os.remove(self.temp_idf_path)

    def run_idf(self, force_run=False):
        if not self.path:
            raise Exception("Can't save, no output directory!")
        if self.is_changed_idf or force_run:
            print("idf has changed - running case")
            try:
                self.idf.run(
                    output_directory=os.path.join(self.path, "results"), verbose="q"
                )
                rprint(
                    f"[bold green] Simulation for case ` {self.path.parent.name}/{self.path.name}` succeeded [/] \n"
                )
            except EnergyPlusRunError:
                self.is_failed_simulation = True
                rprint(
                    f"[bold red] Simulation for case `{self.path}` failed - see error logs [/] \n"
                )

        else:
            print("idf has not changed - no run")

        return True

    def update_weather_and_run_period(self):
        if not self.epw:
            self.epw = EPW(WEATHER_FILE)

        else:
            if isinstance(self.epw, Path):
                self.epw = EPW(self.epw)
            print(f"Got an epw - its {self.epw}")
        self.idf.epw = self.epw.file_path
        self.idf = update_idf_location(self.idf, self.epw)

        if not self.analysis_period:
            self.analysis_period = AnalysisPeriod(
                st_month=7, end_month=7, st_day=1, end_day=1
            )
        self.idf = update_idf_run_period(self.idf, self.analysis_period)



def read_existing_idf(folder_path: Path):
    path = folder_path / DEFAULT_IDF_NAME
    assert path.exists(), "Invalid folder organization!"
    return EneryPlusCaseEditor(starting_path=path)
