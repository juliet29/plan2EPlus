import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import geom

from helpers.helpers import chain_flatten
from helpers.helpers import grouper

HOURS_PER_DAY: int = 24
HOURS_PER_DAY_SECTION: int = HOURS_PER_DAY // 2
INTERVALS_PER_HOUR = 4
INTERVALS_PER_DAY_SECTION = HOURS_PER_DAY_SECTION * INTERVALS_PER_HOUR


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
    a_list = [0] * a
    if not b:
        return a_list

    b_list = [1] * b
    return  a_list + b_list


def create_sched(p_closed, p_open):
    intervs = generate_intervals_two_dist(p_closed, p_open)
    paired_intervs = grouper(intervs, 2)
    return chain_flatten([handle_interv_pair(i) for i in paired_intervs])[0:INTERVALS_PER_DAY_SECTION]

def create_scheds():
    # during the day, can go from open to closed with equal probability 
    day_sched = create_sched(0.2, 0.2)
    # at night, should close with high likelihood after few intervals
    # --- p == 0.1, max of two tries before close 
    # but should open with low probability.. 
    # --- p = 0.8, could take up to 40 intervals before close.. 
    night_sched = create_sched(p_closed=0.1, p_open=0.8)
    hours_chunk = (HOURS_PER_DAY_SECTION//2)*INTERVALS_PER_HOUR
    return night_sched[0:hours_chunk] + day_sched + night_sched[hours_chunk:]

    
