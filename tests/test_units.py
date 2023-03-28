"""
Pytest unit tests for units module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

from pydosa.util.units import decode_unit_prefix
from pydosa.util.units import encode_metric_prefix


def test_decode_unit_prefix():
    """Test decode_unit_prefix method with generic examples"""

    # Without unit prefix
    assert decode_unit_prefix('0') == 0
    assert decode_unit_prefix('12') == 12
    assert decode_unit_prefix('12.3') == 12.3

    # With SI (metric) unit prefix
    assert decode_unit_prefix('12.3k') == 12.3E3
    assert decode_unit_prefix('12.3M') == 12.3E6
    assert decode_unit_prefix('12.3G') == 12.3E9
    assert decode_unit_prefix('-12.3M') == -12.3E6

    # With IEC unit prefix
    assert decode_unit_prefix('4Ki') == 4096
    assert decode_unit_prefix('4Mi') == 4194304
    assert decode_unit_prefix('2Gi') == 2147483648

    # Ignoring specified units
    assert decode_unit_prefix('12.3X', 'X') == 12.3
    assert decode_unit_prefix('12.3kX', 'X') == 12.3E3
    assert decode_unit_prefix('12.3XYZ', 'X') == 12.3
    assert decode_unit_prefix('12.3', 'X') == 12.3

    assert decode_unit_prefix('12.3kX') == 12.3E3
    assert decode_unit_prefix('12.3MX') == 12.3E6
    assert decode_unit_prefix('12.3GX') == 12.3E9


def test_decode_unit_prefix_siglent():
    """Test decode_unit_prefix method with actual Siglent versions"""

    # SARA for SDS1000X-E series
    assert decode_unit_prefix('1.00E+09') == 1E9
    assert decode_unit_prefix('5.00E+08') == 5E8
    assert decode_unit_prefix('2.00E+04') == 2E4

    # SARA for other Siglent models
    assert decode_unit_prefix('1.00GSa/s') == 1E9
    assert decode_unit_prefix('500MSa/s') == 5E8
    assert decode_unit_prefix('20kSa/s') == 2E4

    # SANU for SDS1000X-E
    assert decode_unit_prefix('1.40E+07') == 1.4E7  # SDS1000X-E

    # SANU for SDS2000, SDS2000X, SDS1000X, SDS1000X+
    assert decode_unit_prefix('28Mpts', 'pts') == 2.8E7
    assert decode_unit_prefix('1.4kpts', 'pts') == 1.4E3
    assert decode_unit_prefix('28pts', 'pts') == 2.8E1

    # SANU for other Siglent models
    assert decode_unit_prefix('1600') == 1.6E3


def test_encode_metric_prefix():
    """Test encode_metric_prefix method"""

    # Test scaling and suffix for each decade
    assert encode_metric_prefix(0.0) == "0"
    assert encode_metric_prefix(1.2E-9) == "1.2n"
    assert encode_metric_prefix(1.2E-8) == "12n"
    assert encode_metric_prefix(1.2E-7) == "120n"
    assert encode_metric_prefix(1.2E-6) == "1.2\u03BC"
    assert encode_metric_prefix(1.2E-5) == "12\u03BC"
    assert encode_metric_prefix(1.2E-4) == "120\u03BC"
    assert encode_metric_prefix(1.2E-3) == "1.2m"
    assert encode_metric_prefix(1.2E-2) == "12m"
    assert encode_metric_prefix(1.2E-1) == "120m"
    assert encode_metric_prefix(1.2) == "1.2"
    assert encode_metric_prefix(12) == "12"
    assert encode_metric_prefix(120) == "120"
    assert encode_metric_prefix(1.2E3) == "1.2k"
    assert encode_metric_prefix(1.2E4) == "12k"
    assert encode_metric_prefix(1.2E5) == "120k"
    assert encode_metric_prefix(1.2E6) == "1.2M"
    assert encode_metric_prefix(1.2E7) == "12M"
    assert encode_metric_prefix(1.2E8) == "120M"
    assert encode_metric_prefix(1.2E9) == "1.2G"
    assert encode_metric_prefix(1.2E10) == "12G"
    assert encode_metric_prefix(1.2E11) == "120G"
    assert encode_metric_prefix(1.2E12) == "1.2T"
    assert encode_metric_prefix(1.2E13) == "12T"
    assert encode_metric_prefix(1.2E14) == "120T"

    # Test that out-of-range values are returned in 'E' format
    assert encode_metric_prefix(1.2E-10) == "1.2E-10"
    assert encode_metric_prefix(1.2E15) == "1.2E+15"

    # Test single significant digit does not have trailing ".0"
    assert encode_metric_prefix(1) == "1"
    assert encode_metric_prefix(1E3) == "1k"
    assert encode_metric_prefix(1E4) == "10k"
    assert encode_metric_prefix(1E5) == "100k"

    # Test no rounding with 8 significant digits
    assert encode_metric_prefix(1.2345678) == "1.2345678"
    assert encode_metric_prefix(1.2345678E1) == "12.345678"
    assert encode_metric_prefix(1.2345678E2) == "123.45678"
    assert encode_metric_prefix(1.2345678E3) == "1.2345678k"
    assert encode_metric_prefix(1.2345678E4) == "12.345678k"
    assert encode_metric_prefix(1.2345678E5) == "123.45678k"
    assert encode_metric_prefix(1.2345678E6) == "1.2345678M"
    assert encode_metric_prefix(1.2345678E7) == "12.345678M"
    assert encode_metric_prefix(1.2345678E8) == "123.45678M"

    # Test negative values
    assert encode_metric_prefix(-1.2E-3) == "-1.2m"
    assert encode_metric_prefix(-1.2E-2) == "-12m"
    assert encode_metric_prefix(-1.2E-1) == "-120m"
    assert encode_metric_prefix(-1.2) == "-1.2"
    assert encode_metric_prefix(-1.2e1) == "-12"
    assert encode_metric_prefix(-1.2e2) == "-120"
    assert encode_metric_prefix(-1.2e3) == "-1.2k"
    assert encode_metric_prefix(-1.2e4) == "-12k"
    assert encode_metric_prefix(-1.2e5) == "-120k"

    # Test that out-of-range values are returned in 'E' format
    assert encode_metric_prefix(1.2E-15) == "1.2E-15"
    assert encode_metric_prefix(1.2E15) == "1.2E+15"
    assert encode_metric_prefix(-1.2E-15) == "-1.2E-15"
    assert encode_metric_prefix(-1.2E15) == "-1.2E+15"
