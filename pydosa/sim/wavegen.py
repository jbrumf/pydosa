"""
Signal generator to create test waveforms.

This is intended for generating precise waveforms with known properties
for testing the spectrum analyzer. It can also be used for demonstrating
the analyser when an oscilloscope is not available.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

import numpy as np
from numpy import array as npa

from pydosa.sim.siggen import SigGen, quantize


class WaveGen:
    """Signal generator to create test waveforms."""

    def __init__(self, config):
        """Get settings from configuration file"""
        # FIXME: Type conversions here won't work because sim SETS the values too
        self.config = config
        self.wave: str = config.get('wave')
        self.freq: str = config.get('freq')
        self.dc: str = config.get('dc')
        self.amplitude: str = config.get('amplitude')
        self.units: str = config.get('units')
        self.mod_freq: str = config.get('mod_freq')
        self.mod_depth: str = config.get('mod_depth')  # Percentage
        self.noise: str = config.get('noise')
        self.noise_units: str = config.get('noise_units')
        self.quantization: str = config.get('quantization')  # Volts

        # Create a signal generator
        self.siggen = SigGen()

    def generate(self, nsamples: int, srate: float) -> npa:
        """Generate waveform samples.

        :param nsamples: Number of samples
        :param srate: Sample rate (Sa/s)
        :return: (signal, sample_rate) # Signal in volts

        The signal values are in volts.
        """
        self.siggen.set(nsamples, srate)

        match self.wave:
            case "sine":
                signal = self.siggen.generate_sine(float(self.freq),
                                                   float(self.amplitude), self.units)
                signal = self.siggen.amplitude_modulate(signal, float(self.mod_freq),
                                                        float(self.mod_depth))
            case "square":
                signal = self.siggen.generate_square(float(self.freq))  # No amplitude param
            case "impulse":
                signal = self.siggen.generate_impulse()
            case _:
                raise ValueError("Unknown wave type: ", self.wave)

        noise = self.siggen.generate_noise(float(self.noise), self.noise_units)
        signal += float(self.dc) + noise
        if float(self.quantization) > 0:
            signal = quantize(signal, float(self.quantization))

        return np.array(signal), srate  # Signal units are volts
