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

from pydosa.util.units import decode_unit_prefix

DB3 = 10 * math.log10(2)  # 3dB
Z0 = 50  # Impedance for dBm (ohms)


class WaveGen:
    """Signal generator to create test waveforms."""

    def __init__(self, config):
        """Initialization"""
        self.config = config
        self.wave: str = config.get('wave')
        self.freq: str = config.get('freq')
        self.dc: str = config.get('dc')
        self.amplitude: str = config.get('amplitude')
        self.units: str = config.get('units')
        self.mod_freq: str = config.get('mod_freq')
        self.mod_depth: str = config.get('mod_depth')
        self.noise: str = config.get('noise')
        self.noise_units: str = config.get('noise_units')
        self.delay: str = config.get('delay')
        self.quantization: str = config.get('quantization')  # Volts
        self.nsamples: int = 2
        self.sample_rate: float = 0

    def get_config(self):
        """Get the configuration."""
        return self.config  # FIXME: Just use property?

    def open(self, connection):
        pass

    def close(self):
        pass

    # ---------- Generator implementation ----------

    def generate(self, nsamples: str, srate_option: str):
        """Generate waveform samples.

        :param nsamples: Number of samples
        :param srate_option: Sample rate (Sa/s)
        :return: (signal, sample_rate) # Signal in volts

        The signal values are in volts.
        """
        self.nsamples = nsamples
        self.sample_rate = decode_unit_prefix(srate_option)

        match self.wave:
            case "sine":
                signal = self.generate_sine()
            case "square":
                signal = self.generate_square()
            case "impulse":
                signal = self.generate_impulse()
            case _:
                raise ValueError("Unknown wave type: ", self.wave)

        dc = float(self.dc)
        noise = self.generate_noise()
        quant = float(self.quantization)

        signal = signal + dc + noise
        if quant > 0:
            signal = self.quantize(signal)

        return np.array(signal), self.sample_rate  # Signal units are volts

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

    def generate_sine(self):
        """Generate a sine wave."""
        n = self.nsamples
        freq = float(self.freq)
        srate = float(self.sample_rate)
        amplitude = float(self.amplitude)
        t = np.arange(n) / srate
        volts_pk = self.scale_sine(amplitude, self.units)
        y = np.sin(2 * math.pi * freq * t) * volts_pk
        # Amplitude modulation
        mod_depth = float(self.mod_depth)
        mod_freq = float(self.mod_freq)
        if mod_depth > 0:
            y = y * (1 + mod_depth / 100.0 * np.sin(2 * math.pi * mod_freq * t))
        return y

    def generate_square(self):  # XXX needs checking
        """Generate a square wave."""
        n = self.nsamples
        freq = float(self.freq)
        srate = float(self.sample_rate)
        y = np.zeros(n)
        k = srate / freq
        for i in range(n):
            if i % k < k / 2:
                y[i] = 1.0
        return y

    def generate_impulse(self):
        """Generate an impulse wave."""
        n = self.nsamples
        y = np.zeros(n)
        y[n // 2] = 1
        return y

    def generate_dc(self):
        """Generate a DC value."""
        n = self.nsamples
        return np.full(n, float(self.dc))

    def scale_noise(self, value: float, units: str) -> float:
        """Convert noise amplitude to volts RMS"""
        match units:
            case 'Vrms':
                return value
            case 'dBm':
                return math.sqrt(Z0) * 10 ** ((value - 30) / 20)
            case _:
                raise Exception('Invalid units')

    def generate_noise(self):
        "Generate white noise."""
        noise = float(self.noise)
        volts_rms = self.scale_noise(noise, self.noise_units)
        if volts_rms >= 0:
            return np.random.normal(size=self.nsamples, scale=volts_rms)
        else:
            return np.zeros(self.nsamples)

    # This is only simulating quantization, not clipping (i.e. ADC range)
    def quantize(self, volts: float) -> float:
        """Quantize the values."""
        vpl = float(self.quantization)
        return np.rint(volts / vpl) * vpl

    def show_rms(self, data):
        """Print RMS value for debugging"""
        meansq = np.sum(np.square(data)) / len(data)
        try:
            w = 10.0 * math.log10(meansq / Z0)
            print("Signal: " + repr(w + 30) + " dBm, " + repr(w + 30 - 13) + "dBV")
        except Exception:
            print("Signal: zero")
