"""
Spectrum analyzer that computes FFT etc.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import math
from functools import cache

import numpy as np
import scipy.signal as sig

ALPHA = 0.03  # Averaging: tau / dt = (1 - ALPHA) / ALPHA
DB3 = 10 * math.log10(2)  # 3 dB


@cache
def get_window(name: str, nsamples: int):
    """Return window function and amplitude correction (dB)"""
    match name:
        case 'Hanning':
            return sig.hann(nsamples), 6.021
        case 'Flat-Top':
            return sig.flattop(nsamples), 13.328
        case 'Blackman':
            return sig.blackman(nsamples), 7.535
        case 'Rectangle':
            return None, 0.0
        case _:
            raise ValueError('Unknown window: ', name)


class Analyzer(object):
    """Spectrum analysis"""

    def __init__(self):
        """Initialization"""
        self.__spectrum = None
        self.__count = 0  # Averaging count
        self.last_nsamples = None
        self.last_srate = None
        self.last_window = None
        self.last_mode = None

    def compute_spectrum(self, data, srate: float, mode: str, window: str, units: str):
        """Compute power spectrum"""
        nsamples = len(data)

        # Reset averaging/min/max if invalidated
        if nsamples != (self.last_nsamples
                        or self.last_srate != srate
                        or self.last_mode != mode
                        or self.last_window != window):
            self.__spectrum = None
            self.__count = 0
        self.last_nsamples = nsamples
        self.last_srate = srate
        self.last_mode = mode
        self.last_window = window

        # Apply window function
        winfunc, offset_db = get_window(window, nsamples)
        if winfunc is not None:
            data *= winfunc

        # Do the FFT
        data = np.absolute(np.fft.rfft(data))
        data *= (1 / nsamples)
        # nf = len(data)
        data = data * data  # Need for power averaging. Could be optimized

        # Averaging and max mode (performed on power)
        if self.__spectrum is None:
            self.__spectrum = data
        else:
            match mode:
                case 'Normal':
                    self.__spectrum = data
                case 'Maximum':
                    self.__spectrum = np.maximum(self.__spectrum, data)
                    data = self.__spectrum
                case 'Minimum':
                    self.__spectrum = np.minimum(self.__spectrum, data)
                    data = self.__spectrum
                case 'Average':
                    # Adaptive filter: alpha = 1/2, 1/3, 1/4,... until it reaches ALPHA
                    self.__count += 1
                    alpha = 1.0 / (self.__count + 1)
                    if alpha < ALPHA:
                        alpha = ALPHA
                    self.__spectrum *= (1.0 - alpha)
                    self.__spectrum += data * alpha
                    data = self.__spectrum
                case _:
                    raise ValueError("Unknown mode")

        # Convert to dB
        data += 1E-30  # Avoid divide-by-zero
        data = np.log10(data) * 10.0
        offset_db += DB3  # Double to correct for one-sided spectrum...
        data[0] -= 3.01  # ... except for DC term

        # Scale to required units
        match units:
            case 'dBV':  # RMS
                pass
            case 'dBm':
                offset_db += 10 + DB3  # 1V RMS in 50R = 13.01 dBm
            case 'dBc':
                offset_db = -max(data)
            case _:
                raise ValueError("Unknown unit: ", units)

        data += offset_db  # Apply dB offsets
        return data
