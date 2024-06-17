import re


def get_last_word(string):
    # split by space and converting
    # string to list and
    lis = list(string.split(" "))

    # length of list
    length = len(lis)

    # returning last element in list
    return lis[length - 1]


def to_python_format(text):
    # s = text.replace("-", " ").replace("_", " ")
    return text.replace("-", "_")


INTERSECT_SURF_PATTERN = re.compile("000\d_\d")


def test_intersecting_surface(name):
    return bool(INTERSECT_SURF_PATTERN.match(name[-6:]))
