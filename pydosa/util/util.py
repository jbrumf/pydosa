"""
Utility functions.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import math
import re
from itertools import zip_longest


def round_nice_number(x: float) -> float:
    """ Return the nearest number 'y', such that y=k*10^n,
    where k = 1, 2 or 5 and 'n' is an integer.
    """
    exp = int(math.floor(math.log10(x)))
    f = x / math.pow(10.0, exp)

    if f < 1.5:
        nf = 1.0
    elif f < 3.0:
        nf = 2.0
    elif f < 7.5:
        nf = 5.0
    else:
        nf = 10.0

    return nf * math.pow(10.0, exp)


def ceil_nice_number(x: float) -> float:
    """ Return the smallest number y >= x, such that y=k*10^n,
    where k = 1, 2 or 5 and 'n' is an integer.
    """
    exp = int(math.floor(math.log10(x)))
    f = x / math.pow(10.0, exp)

    if f <= 1.0:
        nf = 1.0
    elif f <= 2.0:
        nf = 2.0
    elif f <= 5.0:
        nf = 5.0
    else:
        nf = 10.0

    return nf * math.pow(10.0, exp)


def floor_nice_number(x: float) -> float:
    """ Return the largest number y <= x, such that y=k*10^n,
    where k = 1, 2 or 5 and 'n' is an integer.
    """
    exp = int(math.floor(math.log10(x)))
    f = x / math.pow(10.0, exp)

    if f < 2.0:
        nf = 1.0
    elif f < 5.0:
        nf = 2.0
    elif f < 10.0:
        nf = 5.0
    else:
        nf = 10.0

    return nf * math.pow(10.0, exp)


def log_ceil(x: float) -> float:
    """ Return the smallest power of 10, >= x.
    """
    return math.pow(10, math.ceil(math.log10(x)))


def log_floor(x: float) -> float:
    """ Return the largest power of 10, <= x.
    """
    return math.pow(10, math.floor(math.log10(x)))


def compatible_version(required: str, actual: str) -> bool:
    """Test that actual version number satisfies the required minimum version.
    """
    pattern = '0*([1-9][0-9]*|[a-zA-Z]+)'
    req = re.findall(pattern, required)
    act = re.findall(pattern, actual)
    ok = True
    for a, r in zip_longest(act, req, fillvalue=''):
        if r.isnumeric() and a.isnumeric():
            if int(a) > int(r):
                return True
            elif int(a) < int(r):
                return False
        else:
            ok &= (r == '' or a == r)
    return ok


def elide_bytes(data: bytes, start: int = 20, stop: int = 3) -> str:
    """Format bytes and elide with ellipsis if too long.
       The whole string is returned if len <= start+stop.
       :param data: The bytes to be formatted
       :param start: Maximum number of bytes at start
       :param stop: Maximum number of bytes at end
       :return: elided string"""
    if len(data) <= start + stop:
        return str(data)
    else:
        first = str(data[0:start])[0:-1]
        last = '' if stop == 0 else str(data[-stop:])[2:]
        return '{} ... {}'.format(first, last)
