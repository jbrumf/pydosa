"""
Pytest unit tests for averager module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

import numpy as np
import numpy.testing as nt

from pydosa.dsa.averager import Averager


class TestAverager:
    data = np.array([[4, 3, 3], [5, 2, 1], [6, 1, 8], [0, 4, 3]], dtype=float)

    def test_normal(self):
        """Test 'Normal; mode"""
        d = np.array(self.data)  # Clone test data
        avr = Averager(0.1)
        x = avr.average(d[0], 'Normal')
        nt.assert_allclose(d[0], x)
        x = avr.average(d[1], 'Normal')
        nt.assert_allclose(d[1], x)
        x = avr.average(d[2], 'Normal')
        nt.assert_allclose(d[2], x)
        nt.assert_allclose(d, self.data)  # Input unchanged

    def test_minimum(self):
        """Test 'Minimum' mode"""
        d = np.array(self.data)  # Clone test data
        avr = Averager(0.1)
        x = avr.average(d[0], 'Minimum')
        nt.assert_allclose(np.array([4, 3, 3]), x)  # First unchanged
        x = avr.average(d[1], 'Minimum')
        nt.assert_allclose(np.array([4, 2, 1]), x)
        x = avr.average(d[2], 'Minimum')
        nt.assert_allclose(np.array([4, 1, 1]), x)
        nt.assert_allclose(d, self.data)  # Input unchanged

    def test_maximum(self):
        """Test 'Maximum' mode"""
        d = np.array(self.data)  # Clone test data
        avr = Averager(0.1)
        x = avr.average(d[0], 'Maximum')
        nt.assert_allclose(np.array([4, 3, 3]), x)  # First unchanged
        x = avr.average(d[1], 'Maximum')
        nt.assert_allclose(np.array([5, 3, 3]), x)
        x = avr.average(d[2], 'Maximum')
        nt.assert_allclose(np.array([6, 3, 8]), x)
        nt.assert_allclose(d, self.data)  # Input unchanged

    def test_average(self):
        """Test 'Average' mode"""
        d = np.array(self.data)  # Clone test data
        avr = Averager(0.2)
        x = avr.average(d[0], 'Average')
        nt.assert_allclose(np.array([4, 3, 3]), x)  # First unchanged
        x = avr.average(d[1], 'Average')
        nt.assert_allclose(sum(d[0:2]) / 2, x)
        x = avr.average(d[2], 'Average')
        nt.assert_allclose(sum(d[0:3]) / 3, x)
        x = avr.average(d[3], 'Average')
        nt.assert_allclose(sum(d[0:4]) / 4, x)
        # Check covergence
        for _ in range(30):
            x = avr.average(d[3], 'Average')
        nt.assert_allclose(d[3], x, atol=0.01)
        nt.assert_allclose(d, self.data)  # Input unchanged

    def test_mode_change(self):
        """Test mode change"""
        d = np.array(self.data)  # Clone test data
        avr = Averager(0.1)
        x = avr.average(d[0], 'Maximum')
        nt.assert_allclose(np.array([4, 3, 3]), x)  # First unchanged
        x = avr.average(d[1], 'Maximum')
        nt.assert_allclose(np.array([5, 3, 3]), x)
        x = avr.average(d[2], 'Minimum')
        nt.assert_allclose(np.array([6, 1, 8]), x)  # Reset of mode change
        x = avr.average(d[3], 'Minimum')
        nt.assert_allclose(np.array([0, 1, 3]), x)
        nt.assert_allclose(d, self.data)  # Input unchanged
