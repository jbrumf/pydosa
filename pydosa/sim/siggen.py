"""
Signal generator to create test waveforms.

This is intended for generating precise waveforms with known properties
for testing the spectrum analyzer. It can also be used for demonstrating
the analyser when an oscilloscope is not available.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import math

import numpy as np
from numpy import array as npa

DB3 = 10 * math.log10(2)  # 3dB
Z0 = 50  # Impedance for dBm (ohms)


class SigGen:
    """Signal generator for test waveforms"""

    def __init__(self):
        self.nsamples = None
        self.srate = None

    def set(self, nsamples: int, srate: float) -> None:
        self.nsamples = nsamples
        self.srate = srate

    def times(self) -> npa:
        # FIXME: cache or save the time array?
        """Return array of times"""
        duration = self.nsamples / self.srate
        return np.linspace(0., duration, num=self.nsamples, endpoint=False)

    def generate_sine(self, freq: float, amplitude: float, units: str = 'Vpk') -> npa:
        """Generate a sine wave."""
        t = self.times()
        volts_pk = self.scale_sine(amplitude, units)
        return np.sin(2 * math.pi * freq * t) * volts_pk

    def amplitude_modulate(self, wave: npa, mod_freq: float, mod_depth: float) -> npa:
        """Amplitude modulation"""
        if math.fabs(mod_depth) < 1e-10:
            return wave
        omega = 2 * math.pi * mod_freq
        t = self.times()
        return wave * (1 + mod_depth / 100.0 * np.sin(omega * t))

    def generate_square(self, freq: float) -> npa:  # XXX needs checking
        """Generate a square wave."""
        n = self.nsamples
        y = np.zeros(n)
        k = self.srate / freq
        for i in range(n):
            if i % k < k / 2:
                y[i] = 1.0
        return y

    def generate_impulse(self) -> npa:
        """Generate an impulse wave."""
        # FIXME: Add arg to specify position of impulse
        n = self.nsamples
        y = np.zeros(n)
        y[n // 2] = 1
        return y

    def generate_dc(self, dc: float) -> npa:
        """Generate a DC value."""
        # It is better to just add a constant to wave
        n = self.nsamples
        return np.full(n, float(dc))

    def generate_noise(self, noise: float, units: str) -> npa:
        "Generate white noise."""
        noise = float(noise)
        volts_rms = self.scale_noise(noise, units)
        if volts_rms >= 0:
            return np.random.normal(size=self.nsamples, scale=volts_rms)
        else:
            return np.zeros(self.nsamples)

    def scale_sine(self, value: float, units: str) -> float:
        """Convert sine amplitude value to volts peak"""
        match units:
            case 'Vpk':
                return value
            case 'dBm':
                return math.sqrt(2 * Z0) * 10 ** ((value - 30) / 20)
            case 'Vrms':
                return value * math.sqrt(2)
            case _:
                raise Exception('Invalid units')

    def scale_noise(self, value: float, units: str) -> float:
        """Convert noise amplitude to volts RMS"""
        match units:
            case 'Vrms':
                return value
            case 'dBm':
                return math.sqrt(Z0) * 10 ** ((value - 30) / 20)
            case _:
                raise Exception('Invalid units')


def times(nsamples: int, srate: float) -> npa:
    """Create numpy array of times"""
    duration = nsamples / srate
    return np.linspace(0., duration, num=nsamples, endpoint=False)


# This is only simulating quantization, not clipping (i.e. ADC range)
def quantize(wave: npa, dv: float) -> npa:
    """Quantize the values."""
    return np.rint(wave / dv) * dv


# ---------- Utility functions ----------

def show_rms(data: npa) -> None:
    """Print RMS value for debugging"""
    meansq = np.sum(np.square(data)) / len(data)
    try:
        w = 10.0 * math.log10(meansq / Z0)
        print("Signal: " + repr(w + 30) + " dBm, " + repr(w + 30 - 13) + "dBV")
    except ValueError:
        print("Signal: zero")
