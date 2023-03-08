"""
Test harnesses for utilities.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import unittest

from pydosa.util.util import ceil_nice_number
from pydosa.util.util import compatible_version
from pydosa.util.util import floor_nice_number
from pydosa.util.util import round_nice_number


class TestUtils(unittest.TestCase):

    def test_round_nice_number(self):
        self.assertEqual(10, round_nice_number(10))
        self.assertEqual(10, round_nice_number(8))
        self.assertEqual(5, round_nice_number(6))
        self.assertEqual(5, round_nice_number(3))
        self.assertEqual(2, round_nice_number(2.9))
        self.assertEqual(2, round_nice_number(1.5))
        self.assertEqual(1, round_nice_number(1.4))

    def test_ceil_nice_number(self):
        self.assertEqual(10, ceil_nice_number(10))
        self.assertEqual(20, ceil_nice_number(11))
        self.assertEqual(20, ceil_nice_number(20))
        self.assertEqual(50, ceil_nice_number(21))
        self.assertEqual(50, ceil_nice_number(50))
        self.assertEqual(100, ceil_nice_number(51))
        self.assertEqual(100, ceil_nice_number(99))

    def test_floor_nice_number(self):
        self.assertEqual(10, floor_nice_number(10))
        self.assertEqual(10, floor_nice_number(11))
        self.assertEqual(10, floor_nice_number(19))
        self.assertEqual(20, floor_nice_number(20))
        self.assertEqual(20, floor_nice_number(49))
        self.assertEqual(50, floor_nice_number(50))
        self.assertEqual(50, floor_nice_number(99))

    def test_compatible_version(self):
        # Test with generic patterns
        self.assertTrue(compatible_version('1.2.3', '1.2.3'))
        self.assertTrue(compatible_version('1.2.3', '1.2.4'))
        self.assertFalse(compatible_version('1.2.4', '1.2.3'))
        self.assertTrue(compatible_version('1.2', '1.2.3'))
        self.assertTrue(compatible_version('1.2.3', '1.2.3.4'))
        self.assertTrue(compatible_version('1.2.3', '1.3.2'))
        self.assertTrue(compatible_version('1.2.3', '1.3.2.1'))
        self.assertTrue(compatible_version('1.2.3', '1.2.3R2'))
        self.assertFalse(compatible_version('1.2.3R2', '1.2.3'))
        self.assertTrue(compatible_version('1.2.3R1', '1.2.3R2'))
        self.assertFalse(compatible_version('1.2.3R2', '1.2.3R1'))
        self.assertTrue(compatible_version('1.2.3', '1.2.3SP2'))
        self.assertFalse(compatible_version('1.2.3SP2', '1.2.3'))
        self.assertTrue(compatible_version('1.2.3SP1', '1.2.3SP2'))
        self.assertFalse(compatible_version('1.2.3SP2', '1.2.3SP1'))

        # Lexicographical ordering does NOT support the following:
        # self.assertTrue(compatible_version('1.2.3', '1.2.03'))
        # self.assertTrue(compatible_version('1.2.3', '1.2.12'))
        # self.assertTrue(compatible_version('1.2.3RC1', '1.2.3'))

        # Test with actual Siglent version numbers
        self.assertFalse(compatible_version('7.1.6.1.33', '7.1.6.1.26'))
        self.assertTrue(compatible_version('7.1.6.1.33', '7.1.6.1.35R2'))

        # Test with actual Rigol version numbers
        self.assertTrue(compatible_version('00.04.04.03.02', '00.04.04.04.03'))
        self.assertTrue(compatible_version('00.04.04.03.02', '00.04.04.03.02'))
        self.assertTrue(compatible_version('00.04.03.02.03', '00.04.03.SP1'))
        self.assertFalse(compatible_version('00.04.03.SP1', '00.04.03.02.03'))


if __name__ == "__main__":
    unittest.main()
