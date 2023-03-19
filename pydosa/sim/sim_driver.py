"""
Adapter to make a WaveGen look like an instrument driver.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

from pydosa.dsa.scope_driver import ScopeDriver
from pydosa.util.units import decode_unit_prefix

class SimDriver(ScopeDriver):
    """Adapter to make the WaveGen look like an instrument driver."""

    # Dummy instrument definitions
    make = ''
    models = []
    min_firmware = ''

    # Items for instrument-specific menus
    sample_rates = ['1G', '500M', '250M', '100M', '50M', '20M']
    sample_sizes = ['1ki', '2ki', '4ki', '8ki', '16ki', '32ki', '64ki', '128ki', '256ki', '512ki',
                    '1Mi', '2Mi', '4Mi', '8Mi', '12Mi', '14M']
    initial_sample_size = '1Mi'

    def __init__(self, wavegen):
        """Initialization"""
        self.wavegen = wavegen

    def open(self, connection):
        pass

    def prepare(self):
        pass

    def fetch_data(self, nsamples, srate_option):
        srate = decode_unit_prefix(srate_option)
        return self.wavegen.generate(nsamples, srate)

    def close(self):
        """Close the WaveGen."""
        pass
