"""
Pytest unit tests for analyzer module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

import math

import numpy as np
import numpy.testing as nt

from pydosa.dsa.analyzer import Analyzer, get_window


def db2pwr(dbs):
    """Convert dB into power ratio."""
    return 10 ** (dbs / 10)


class TestAnalyzer:
    data = np.array([[0, 1, 2, 3, 4, 5, 6, 7]], dtype=float)

    def test_zeros(self):
        """Test on array of zeros"""
        anlzr = Analyzer()
        n = 8
        d = np.zeros(n)
        spectrum, srate = anlzr.compute_spectrum(d, 1, 'Normal', 'Rectangle')
        nt.assert_allclose(db2pwr(spectrum), np.zeros(n // 2 + 1), atol=1e-10)

    def test_1(self):
        """Test on a single impulse"""
        anlzr = Analyzer()
        d = np.array([1, 0, 0, 0, 0, 0, 0, 0], dtype=float)
        n = len(d)
        spectrum, srate = anlzr.compute_spectrum(d, 1, 'Normal', 'Rectangle')
        power = db2pwr(spectrum)
        # nt.assert_allclose(power, np.array([1, 2, 2, 2, 1])/64, atol=1E-4)
        nt.assert_allclose(power, np.array([1, 2, 2, 2, 2]) / 64, atol=1E-4)

    # Note: Strictly, the Nyquist frequency term should be halved for even 'n'

    def test_2(self):
        """Test on cosine wave of 1 cycle"""
        anlzr = Analyzer()
        n = 8
        d = np.cos(np.arange(n) * (2 * math.pi / n)) * math.sqrt(2)  # RMS = 1
        spectrum, srate = anlzr.compute_spectrum(d, 1, 'Normal', 'Rectangle')
        power = db2pwr(spectrum)
        nt.assert_allclose(np.sum(power), 1)
        nt.assert_allclose(power, np.array([0, 1.0, 0, 0, 0]), atol=1E-4)

    def test_get_window(self):
        n = 1000
        # Integrate window and check gain
        for name in ['Hanning', 'Flat-Top', 'Blackman']:
            win, loss = get_window(name, n)
            gain = 20 * math.log10(sum(win) / n)
            print('\n', loss, gain)
            nt.assert_almost_equal(loss, -gain, decimal=2)
