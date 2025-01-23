from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import geom
import polars as pl
from geomeppy import IDF
from eppy.bunch_subclass import EpBunch

from ...helpers.helpers import chain_flatten
from ...helpers.helpers import grouper
from ladybug.analysisperiod import AnalysisPeriod

HOURS_PER_DAY: int = 24
HOURS_PER_DAY_SECTION: int = HOURS_PER_DAY // 2
INTERVALS_PER_HOUR = 4
INTERVALS_PER_DAY_SECTION = HOURS_PER_DAY_SECTION * INTERVALS_PER_HOUR
INTERVALS_PER_DAY = HOURS_PER_DAY * INTERVALS_PER_HOUR
YEAR_LEN = 365

OPEN_CODE = 1
CLOSED_CODE = 0


def plot_geom_dist(p=0.1):
    fig, ax = plt.subplots(1, 1)
    x = np.arange(geom.ppf(0.01, p), geom.ppf(0.99, p))
    ax.plot(x, geom.pmf(x, p), "bo", ms=8, label=f"geom pmf, p={p}")
    ax.vlines(x, 0, geom.pmf(x, p), colors="b", lw=5, alpha=0.5)
    ax.legend(loc="best", frameon=False)
    plt.show()

    return fig


def generate_intervals_two_dist(p_closed, p_open):
    # geom dist=> number of tries until success
    rv_closed = geom(p_closed)
    rv_open = geom(p_open)

    times = []
    time_periods_elapsed = 0
    ix_tracker = 0

    while time_periods_elapsed < INTERVALS_PER_DAY_SECTION:
        is_open = ix_tracker % 2
        val = rv_open.rvs() if is_open else rv_closed.rvs()
        times.append(val)
        time_periods_elapsed += val
        ix_tracker += 1

    return times


def handle_interv_pair(pair: tuple[int, int | None]):
    a, b = pair
    a_list = [CLOSED_CODE] * a
    if not b:
        return a_list

    b_list = [OPEN_CODE] * b
    return a_list + b_list


def create_partial_day_sched(p_closed, p_open):
    intervs = generate_intervals_two_dist(p_closed, p_open)
    paired_intervs = grouper(intervs, 2)
    return chain_flatten([handle_interv_pair(i) for i in paired_intervs])[
        0:INTERVALS_PER_DAY_SECTION
    ]


def create_day_sched():
    # during the day, can go from open to closed with equal probability
    day_sched = create_partial_day_sched(0.2, 0.2)
    # at night, should close with high likelihood after few intervals
    # --- p == 0.1, max of two tries before close
    # but should open with low probability..
    # --- p = 0.8, could take up to 40 intervals before close..
    night_sched = create_partial_day_sched(p_closed=0.1, p_open=0.8)
    hours_chunk = (HOURS_PER_DAY_SECTION // 2) * INTERVALS_PER_HOUR
    return night_sched[0:hours_chunk] + day_sched + night_sched[hours_chunk:]


def create_year_sched():
    # TODO import from elsewhere?
    ap = AnalysisPeriod(st_month=6, end_month=10, timestep=INTERVALS_PER_HOUR)
    start_day, end_day = ap.doys_int[0], ap.doys_int[-1]
    ap_sched = chain_flatten([create_day_sched() for i in ap.doys_int])

    before_sched = [OPEN_CODE] * (start_day - 1) * HOURS_PER_DAY * INTERVALS_PER_HOUR
    after_sched = (
        [OPEN_CODE] * (YEAR_LEN - end_day) * HOURS_PER_DAY * INTERVALS_PER_HOUR
    )

    year_sched = before_sched + ap_sched + after_sched

    assert len(before_sched) + len(ap.hoys_int) + len(after_sched) == len(year_sched)

    return year_sched


def create_door_status_csv(path: Path, file_name: str):
    file_path = path / f"{file_name}.csv"
    sched = create_year_sched()
    df = pl.DataFrame(data={"door_state": sched})
    df.write_csv(file=file_path)

    return file_path


def add_venting_sched_object(idf: IDF, path: Path, afn_surface: EpBunch):
    file_name = "_".join(afn_surface.Surface_Name.split(" "))
    file_path = create_door_status_csv(path, file_name)

    o = idf.newidfobject("SCHEDULE:FILE")
    o.File_Name = str(file_path)
    o.Name = f"VentSched_{file_name}"
    o.Minutes_per_Item = 15
    o.Rows_to_Skip_at_Top = 1
    o.Column_Number = 1

    afn_surface.Venting_Availability_Schedule_Name = o.Name
    afn_surface.Ventilation_Control_Mode = "Constant"

    return idf


def add_dynamic_vent_sched_to_doors(idf: IDF, idf_path: Path):
    doors = [
        i
        for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
        if "Door" in i.Surface_Name
    ]
    for door in doors:
        idf = add_venting_sched_object(idf, idf_path.parent, door)
    return idf


def close_doors(idf: IDF):
    doors = [
        i
        for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
        if "Door" in i.Surface_Name
    ]
    for door in doors:
        door.Ventilation_Control_Mode = "NoVent"

    return idf
