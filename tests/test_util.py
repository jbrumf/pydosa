"""
Pytest unit tests for util module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

from pydosa.util.util import ceil_nice_number
from pydosa.util.util import compatible_version
from pydosa.util.util import floor_nice_number
from pydosa.util.util import round_nice_number


def test_round_nice_number():
    assert round_nice_number(10) == 10
    assert round_nice_number(8) == 10
    assert round_nice_number(6) == 5
    assert round_nice_number(3) == 5
    assert round_nice_number(2.9) == 2
    assert round_nice_number(1.5) == 2
    assert round_nice_number(1.4) == 1


def test_ceil_nice_number():
    assert ceil_nice_number(10) == 10
    assert ceil_nice_number(11) == 20
    assert ceil_nice_number(20) == 20
    assert ceil_nice_number(21) == 50
    assert ceil_nice_number(50) == 50
    assert ceil_nice_number(51) == 100
    assert ceil_nice_number(99) == 100


def test_floor_nice_number():
    assert floor_nice_number(10) == 10
    assert floor_nice_number(11) == 10
    assert floor_nice_number(19) == 10
    assert floor_nice_number(20) == 20
    assert floor_nice_number(49) == 20
    assert floor_nice_number(50) == 50
    assert floor_nice_number(99) == 50


def test_compatible_version():
    # Test with generic patterns
    assert compatible_version('1.2.3', '1.2.3')
    assert compatible_version('1.2.3', '1.2.4')
    assert not compatible_version('1.2.4', '1.2.3')
    assert compatible_version('1.2', '1.2.3')
    assert compatible_version('1.2.3', '1.2.3.4')
    assert compatible_version('1.2.3', '1.3.2')
    assert compatible_version('1.2.3', '1.3.2.1')
    assert compatible_version('1.2.3', '1.2.3R2')
    assert not compatible_version('1.2.3R2', '1.2.3')
    assert compatible_version('1.2.3R1', '1.2.3R2')
    assert not compatible_version('1.2.3R2', '1.2.3R1')
    assert compatible_version('1.2.3', '1.2.3SP2')
    assert not compatible_version('1.2.3SP2', '1.2.3')
    assert compatible_version('1.2.3SP1', '1.2.3SP2')
    assert not compatible_version('1.2.3SP2', '1.2.3SP1')

    # Lexicographical ordering does NOT support the following:
    # assert compatible_version('1.2.3', '1.2.03')
    # assert compatible_version('1.2.3', '1.2.12')
    # assert compatible_version('1.2.3RC1', '1.2.3')

    # Test with actual Siglent version numbers
    assert not compatible_version('7.1.6.1.33', '7.1.6.1.26')
    assert compatible_version('7.1.6.1.33', '7.1.6.1.35R2')

    # Test with actual Rigol version numbers
    assert compatible_version('00.04.04.03.02', '00.04.04.04.03')
    assert compatible_version('00.04.04.03.02', '00.04.04.03.02')
    assert compatible_version('00.04.03.02.03', '00.04.03.SP1')
    assert not compatible_version('00.04.03.SP1', '00.04.03.02.03')
