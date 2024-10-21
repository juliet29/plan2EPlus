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


def chain_flatten(lst: Iterable[Iterable[T]]) -> Iterable[T]:
    return list(chain.from_iterable(lst))

def filter_none(lst: Iterable[T|None]) -> List[T]:
    return [i for i in lst if i]

def set_difference(s_large:Iterable, s2:Iterable):
    return list(set(s_large).difference(set(s2)))

def list_all_dict_values(d:dict):
    return chain_flatten([v for v in d.values()])