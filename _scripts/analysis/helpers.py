import polars as pl
from helpers.ep_helpers import get_zone_num
from helpers.geometry_interfaces import Domain




def get_domains_lim(zone_domains: list[Domain]):
    PAD = 1.4 * 1.1
    min_x = min([i.width.min for i in zone_domains]) - PAD
    max_x = max([i.width.max for i in zone_domains]) + PAD
    min_y = min([i.height.min for i in zone_domains]) - PAD
    max_y = max([i.height.max for i in zone_domains]) + PAD
    return (min_x, max_x), (min_y, max_y)


def get_min_max_values(medians: pl.DataFrame, col=None):
    if not col:
        numeric_values = medians.select(pl.selectors.numeric())
        min_val = numeric_values.min_horizontal().min()
        max_val = numeric_values.max_horizontal().max()

    else:
        series = medians[col]
        return series.min(), series.max()

    return min_val, max_val


def true_min_max(min_max_pairs: list[tuple[float, float]]):
    min_val = min([m[0] for m in min_max_pairs])
    max_val = max([m[1] for m in min_max_pairs])
    return min_val, max_val


def convert_zone_space_name(room_map: dict[int, str], name):
    try:
        ix = get_zone_num(name)
        room_name = room_map[ix]
        return f"{ix}-{room_name}"
    except:
        return name
