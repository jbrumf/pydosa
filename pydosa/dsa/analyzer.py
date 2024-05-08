"""
Spectrum analyzer that computes FFT etc.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

import math
from functools import cache

import numpy as np
import scipy.signal as sig
from numpy import array as npa

from pydosa.dsa.averager import Averager

ALPHA = 0.03  # Averaging: tau / dt = (1 - ALPHA) / ALPHA
DB3 = 10 * math.log10(2)  # 3 dB


@cache
def get_window(name: str, nsamples: int) -> npa:
    """Return window function and its coherent power loss (dB)"""
    match name:
        case 'Hanning':
            return sig.windows.hann(nsamples), 6.021
        case 'Flat-Top':
            return sig.windows.flattop(nsamples), 13.328
        case 'Blackman':
            return sig.windows.blackman(nsamples), 7.535
        case 'Rectangle':
            return None, 0.0
        case _:
            raise ValueError('Unknown window: ', name)


class Analyzer(object):
    """Spectrum analysis"""

    def __init__(self):
        """Initialization"""
        self.averager = Averager(ALPHA)
        self.last_nsamples = None
        self.last_srate = None
        self.last_window = None
        self.last_mode = None

    def compute_spectrum(self, data, srate: float, mode: str, window: str) -> tuple[npa, float]:
        """Compute power spectrum in dBV"""
        nsamples = len(data)

        # Apply window function
        winfunc, offset_db = get_window(window, nsamples)
        if winfunc is not None:
            data *= winfunc

        # Do the FFT
        data = np.absolute(np.fft.rfft(data, norm='forward'))
        data = data * data  # Needed for power averaging
        monitor = (nsamples, srate, window)  # Reset average if this changes
        data = self.averager.average(data, mode, monitor)

        # Convert to dBV
        data += 1E-30  # Avoid divide-by-zero
        data = np.log10(data) * 10.0
        offset_db += DB3  # Double to correct for one-sided spectrum...
        data[0] -= 3.01  # ... except for DC term
        data += offset_db  # Apply dB offsets

        return data, srate
