from typing import Dict
from itertools import chain, groupby, tee
from typing import Any, Callable, Dict, Iterable, List, TypeVar, Union


T = TypeVar("T")

def min_max_norm(val, min, max):
    return (val - min)/(max - min)


def key_from_value(dict:Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]



def sort_and_group_objects(lst: Iterable[T], fx: Callable[[T], Any]) -> List[List[T]]:
    sorted_objs = sorted(lst, key=fx)
    return [list(g) for _, g in groupby(sorted_objs, fx)]


def sort_and_group_objects_dict(lst: Iterable[T], fx: Callable[[T], Any]) :
    sorted_objs = sorted(lst, key=fx)
    groups = []
    uniquekeys = []
    for k, g in groupby(sorted_objs, fx):
        groups.append(list(g))
        uniquekeys.append(k)

    return uniquekeys, groups
