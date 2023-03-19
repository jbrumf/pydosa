"""
Utility functions.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import math


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

    For example: compatible_version('7.1.6.1.33', '7.1.6.1.35R2').
    Lexicographical ordering is assumed for each version field.
    """
    req = required.split(',')
    act = actual.split(',')
    return act >= req
