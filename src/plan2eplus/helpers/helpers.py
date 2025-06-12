from typing import Dict, Optional, Protocol
from itertools import chain, groupby, tee, zip_longest
from typing import Any, Callable, Dict, Iterable, List, TypeVar, Union
import re
from dataclasses import fields

import polars as pl


T = TypeVar("T")


def min_max_norm(val, min, max):
    return (val - min) / (max - min)


def key_from_value(dict: Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]


def sort_and_group_objects(lst: Iterable[T], fx: Callable[[T], Any]) -> List[List[T]]:
    sorted_objs = sorted(lst, key=fx)
    return [list(g) for _, g in groupby(sorted_objs, fx)]

def sort_and_group_objects_dict(lst: Iterable[T], fx: Callable[[T], Any]) -> dict[T, list[T]]:
    sorted_objs = sorted(lst, key=fx)
    d = {}
    for k, g in groupby(sorted_objs, fx):
        d[k] = [i for i in list(g)]
    return d




def dataclass_as_dict(dataclass):
    return {field.name: getattr(dataclass, field.name) for field in fields(dataclass)}





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


def regex_tester(pattern_str:str, test_name:str):
    print(f"Looking for {test_name}")
    pattern = re.compile(pattern_str)
    m = pattern.search(test_name)
    print(m)

    if m:
        print(m.group())
        return m.group()
    else:
        print("No match found!")
    
def regex_match(pattern_str:str, value:str, IGNORE_CASE=False):
    if IGNORE_CASE:
        pattern = re.compile(pattern_str, re.IGNORECASE)
    else:
        pattern = re.compile(pattern_str)
    m = pattern.search(value)
    if m:
        return m.group()
    else:
        return None


# def pairwise(iterable):
#     "s -> (s0, s1), (s1, s2), (s2, s3), ..."
#     a, b = tee(iterable)
#     next(b, None)
#     return zip(a, b)
