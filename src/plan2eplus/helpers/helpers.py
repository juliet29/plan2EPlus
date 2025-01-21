from typing import Dict
from itertools import chain, groupby, tee, zip_longest
from typing import Any, Callable, Dict, Iterable, List, TypeVar, Union

import polars as pl


T = TypeVar("T")


def min_max_norm(val, min, max):
    return (val - min) / (max - min)


def key_from_value(dict: Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]


def sort_and_group_objects(lst: Iterable[T], fx: Callable[[T], Any]) -> List[List[T]]:
    sorted_objs = sorted(lst, key=fx)
    return [list(g) for _, g in groupby(sorted_objs, fx)]


def chain_flatten(lst: Iterable[Iterable[T]]) -> List[T]:
    return list(chain.from_iterable(lst))


def filter_none(lst: Iterable[T | None]) -> List[T]:
    return [i for i in lst if i]


def set_difference(s_large: Iterable, s2: Iterable):
    return list(set(s_large).difference(set(s2)))


def set_union(s1: Iterable, s2: Iterable):
    return list(set(s1).union(set(s2)))


def list_all_dict_values(d: dict):
    return chain_flatten([v for v in d.values()])


def get_min_max_values(medians: pl.DataFrame, col=None):
    if not col:
        numeric_values = medians.select(pl.selectors.numeric())
        min_val = numeric_values.min_horizontal().min()
        max_val = numeric_values.max_horizontal().max()

    else:
        series = medians[col]
        return series.min(), series.max()

    return min_val, max_val


class ContainsAsEqualsString(str):
    def __eq__(self, other):
        return self.__contains__(other)


def grouper(iterable, n):
    "Collect data into non-overlapping fixed-length chunks or blocks."
    # grouper('ABCDEFG', 3, incomplete='ignore') → ABC DEF
    iterators = [iter(iterable)] * n
    return list(zip_longest(*iterators, fillvalue=None))
