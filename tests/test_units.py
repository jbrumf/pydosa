"""
Test harnesses for units utilities.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import unittest

from pydosa.util.units import decode_unit_prefix
from pydosa.util.units import encode_metric_prefix


class TestUnits(unittest.TestCase):

    def test_decode_unit_prefix(self):
        # Without unit prefix
        self.assertEqual(0, decode_unit_prefix('0'))
        self.assertEqual(12, decode_unit_prefix('12'))
        self.assertEqual(12.3, decode_unit_prefix('12.3'))

        # With SI (metric) unit prefix
        self.assertEqual(12.3E3, decode_unit_prefix('12.3k'))
        self.assertEqual(12.3E6, decode_unit_prefix('12.3M'))
        self.assertEqual(12.3E9, decode_unit_prefix('12.3G'))
        self.assertEqual(-12.3E6, decode_unit_prefix('-12.3M'))

        # With IEC unit prefix
        self.assertEqual(4096, decode_unit_prefix('4Ki'))
        self.assertEqual(4194304, decode_unit_prefix('4Mi'))
        self.assertEqual(2147483648, decode_unit_prefix('2Gi'))

        # Ignoring specified units
        self.assertEqual(12.3, decode_unit_prefix('12.3X', 'X'))
        self.assertEqual(12.3E3, decode_unit_prefix('12.3kX', 'X'))
        self.assertEqual(12.3, decode_unit_prefix('12.3XYZ', 'X'))
        self.assertEqual(12.3, decode_unit_prefix('12.3', 'X'))

        self.assertEqual(12.3E3, decode_unit_prefix('12.3kX'))
        self.assertEqual(12.3E6, decode_unit_prefix('12.3MX'))
        self.assertEqual(12.3E9, decode_unit_prefix('12.3GX'))

    def test_decode_unit_prefix_siglent(self):
        # SARA for SDS1000X-E series
        self.assertEqual(1E9, decode_unit_prefix('1.00E+09'))
        self.assertEqual(5E8, decode_unit_prefix('5.00E+08'))
        self.assertEqual(2E4, decode_unit_prefix('2.00E+04'))

        # SARA for other Siglent models
        self.assertEqual(1E9, decode_unit_prefix('1.00GSa/s'))
        self.assertEqual(5E8, decode_unit_prefix('500MSa/s'))
        self.assertEqual(2E4, decode_unit_prefix('20kSa/s'))

        # SANU for SDS1000X-E
        self.assertEqual(1.4E7, decode_unit_prefix('1.40E+07'))  # SDS1000X-E

        # SANU for SDS2000, SDS2000X, SDS1000X, SDS1000X+
        self.assertEqual(2.8E7, decode_unit_prefix('28Mpts', 'pts'))
        self.assertEqual(1.4E3, decode_unit_prefix('1.4kpts', 'pts'))
        self.assertEqual(2.8E1, decode_unit_prefix('28pts', 'pts'))

        # SANU for other Siglent models
        self.assertEqual(1.6E3, decode_unit_prefix('1600'))

    def test_encode_metric_prefix(self):
        # Test scaling and suffix for each decade
        self.assertEqual("0", encode_metric_prefix(0.0))
        self.assertEqual("1.2n", encode_metric_prefix(1.2E-9))
        self.assertEqual("12n", encode_metric_prefix(1.2E-8))
        self.assertEqual("120n", encode_metric_prefix(1.2E-7))
        self.assertEqual("1.2\u03BC", encode_metric_prefix(1.2E-6))
        self.assertEqual("12\u03BC", encode_metric_prefix(1.2E-5))
        self.assertEqual("120\u03BC", encode_metric_prefix(1.2E-4))
        self.assertEqual("1.2m", encode_metric_prefix(1.2E-3))
        self.assertEqual("12m", encode_metric_prefix(1.2E-2))
        self.assertEqual("120m", encode_metric_prefix(1.2E-1))
        self.assertEqual("1.2", encode_metric_prefix(1.2))
        self.assertEqual("12", encode_metric_prefix(12))
        self.assertEqual("120", encode_metric_prefix(120))
        self.assertEqual("1.2k", encode_metric_prefix(1.2E3))
        self.assertEqual("12k", encode_metric_prefix(1.2E4))
        self.assertEqual("120k", encode_metric_prefix(1.2E5))
        self.assertEqual("1.2M", encode_metric_prefix(1.2E6))
        self.assertEqual("12M", encode_metric_prefix(1.2E7))
        self.assertEqual("120M", encode_metric_prefix(1.2E8))
        self.assertEqual("1.2G", encode_metric_prefix(1.2E9))
        self.assertEqual("12G", encode_metric_prefix(1.2E10))
        self.assertEqual("120G", encode_metric_prefix(1.2E11))
        self.assertEqual("1.2T", encode_metric_prefix(1.2E12))
        self.assertEqual("12T", encode_metric_prefix(1.2E13))
        self.assertEqual("120T", encode_metric_prefix(1.2E14))

        # Test that out-of-range values are returned in 'E' format
        self.assertEqual("1.2E-10", encode_metric_prefix(1.2E-10))
        self.assertEqual("1.2E+15", encode_metric_prefix(1.2E15))

        # Test single significant digit does not have trailing ".0"
        self.assertEqual("1", encode_metric_prefix(1))
        self.assertEqual("1k", encode_metric_prefix(1E3))
        self.assertEqual("10k", encode_metric_prefix(1E4))
        self.assertEqual("100k", encode_metric_prefix(1E5))

        # Test no rounding with 8 significant digits
        self.assertEqual("1.2345678", encode_metric_prefix(1.2345678))
        self.assertEqual("12.345678", encode_metric_prefix(1.2345678E1))
        self.assertEqual("123.45678", encode_metric_prefix(1.2345678E2))
        self.assertEqual("1.2345678k", encode_metric_prefix(1.2345678E3))
        self.assertEqual("12.345678k", encode_metric_prefix(1.2345678E4))
        self.assertEqual("123.45678k", encode_metric_prefix(1.2345678E5))
        self.assertEqual("1.2345678M", encode_metric_prefix(1.2345678E6))
        self.assertEqual("12.345678M", encode_metric_prefix(1.2345678E7))
        self.assertEqual("123.45678M", encode_metric_prefix(1.2345678E8))

        # Test negative values
        self.assertEqual("-1.2m", encode_metric_prefix(-1.2E-3))
        self.assertEqual("-12m", encode_metric_prefix(-1.2E-2))
        self.assertEqual("-120m", encode_metric_prefix(-1.2E-1))
        self.assertEqual("-1.2", encode_metric_prefix(-1.2))
        self.assertEqual("-12", encode_metric_prefix(-1.2e1))
        self.assertEqual("-120", encode_metric_prefix(-1.2e2))
        self.assertEqual("-1.2k", encode_metric_prefix(-1.2e3))
        self.assertEqual("-12k", encode_metric_prefix(-1.2e4))
        self.assertEqual("-120k", encode_metric_prefix(-1.2e5))

        # Test that out-of-range values are returned in 'E' format
        self.assertEqual("1.2E-15", encode_metric_prefix(1.2E-15))
        self.assertEqual("1.2E+15", encode_metric_prefix(1.2E15))
        self.assertEqual("-1.2E-15", encode_metric_prefix(-1.2E-15))
        self.assertEqual("-1.2E+15", encode_metric_prefix(-1.2E15))


if __name__ == "__main__":
    unittest.main()
