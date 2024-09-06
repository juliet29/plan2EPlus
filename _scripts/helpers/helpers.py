from typing import Dict
def min_max_norm(val, min, max):
    return (val - min)/(max - min)


def key_from_value(dict:Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]




