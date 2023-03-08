"""
Utility functions for units.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

UNIT_PREFIXES = {'Gi': 1073741824, 'G': 1E9, 'Mi': 1048576, 'M': 1E6, 'Ki': 1024,
                 'k': 1000}
METRIC_SUFFIXES = ['n', '\u03BC', 'm', '', 'k', 'M', 'G', 'T']


def decode_unit_prefix(string: str, delim='') -> float:
    """Decode value with IEC unit prefix (Gi, Mi, Ki) or SI prefix (G, M, k)."""
    n = string.find(delim)
    if n > 0:
        string = string[0:n]
    for prefix in UNIT_PREFIXES.keys():
        if prefix in string:
            return float(string.split(prefix)[0]) * UNIT_PREFIXES[prefix]
    return float(string)


def encode_metric_prefix(value) -> str:
    """Encode number using metric (SI) unit prefix (e.g. m, k, M, G)."""
    s = "%.8E" % value
    x = s.split('E')
    n = int(x[1])
    if n < -9 or n > 14:
        return "%G" % value  # Use G format if prefix not supported
    k = n // 3
    m = n % 3
    f = float(x[0])
    if m == 1:
        f *= 10
    elif m == 2:
        f *= 100
    return '%.8g' % f + METRIC_SUFFIXES[k + 3]
