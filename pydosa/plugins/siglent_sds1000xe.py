"""
Driver for Siglent SDS1000X-E series oscilloscopes.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

import time

import numpy as np

from pydosa.dsa.scope_driver import ScopeDriver
from pydosa.util.units import decode_unit_prefix


class Driver(ScopeDriver):
    """Driver for the Siglent SDS1000X-E series oscilloscope."""

    # Instruments supported by this driver
    make = 'Siglent'
    models = ['SDS1104X-E', 'SDS1204X-E', 'SDS1104X-U']
    min_firmware = '7.3.6.1.37R9'

    # Sample rates and corresponding times per division
    SRATE_TO_TDIV = {'1G': '1E-3', '500M': '2E-3', '250M': '5E-3',
                     '100M': '1E-2', '50M': '2E-2', '20M': '5E-2'}

    # Items for instrument-specific menus
    sample_rates = list(SRATE_TO_TDIV)
    sample_sizes = ['1Mi', '2Mi', '4Mi', '8Mi', '12Mi', '14M']
    initial_sample_size = '1Mi'

    def __init__(self):
        """Initialization"""
        self._scope = None
        self.nsamples = 0

    def open(self, instrument) -> None:
        """Open the driver."""
        self._scope = instrument

    def prepare(self) -> None:
        """Configure the oscilloscope."""
        self._scope.write('STOP')  # Put scope in a known state
        self._scope.write('TRMD SINGLE')
        self._scope.write('ACQW SAMPLING')  # Normal acquisition mode
        self._scope.write('MSIZ 14M')  # Must not be stopped for this
        self._scope.write('STOP')
        self._scope.write('CHDR OFF')  # Don't return headers
        self._scope.write('C1:TRA ON')  # Channel 1 only
        self._scope.write('C2:TRA OFF')
        self._scope.write('C3:TRA OFF')
        self._scope.write('C4:TRA OFF')
        self._scope.write('C1:UNIT V')
        self._scope.write('TDIV 1E-3')
        _ = self._scope.ask('INR?')  # Clear status

    def fetch_data(self, nsamples: int, srate_option: str) -> tuple[np.array, float]:
        """Acquire sample data, scaled to volts"""
        self.nsamples = nsamples
        tdiv = self.SRATE_TO_TDIV[srate_option]
        self._scope.write('TDIV ' + tdiv)
        self._scope.write('TRMD SINGLE')
        _ = self._scope.ask('INR?')  # Clear status
        self._scope.write('ARM')

        # Wait for acquisition to complete
        for i in range(100):
            inr = int(self._scope.ask('INR?'))
            if inr & 1 == 1:
                break
            time.sleep(0.02)

        # Get the samples from the scope and scale to volts
        self._scope.write('WFSU SP,1,NP,{},FP,0'.format(self.nsamples))
        self._scope.write('C1:WF? DAT2')
        data = self._scope.read_raw()
        vdiv = float(self._scope.ask('C1:VDIV?'))
        ofst = float(self._scope.ask('C1:OFST?'))
        sara = decode_unit_prefix(self._scope.ask('SARA?'))
        data = np.array(bytearray(data), dtype=np.int8)[16:-2]
        data = data * (vdiv / 25.0) + ofst
        return data, sara

    def close(self) -> None:
        """Close the driver."""
        if self._scope:
            self._scope.write('TRMD AUTO')  # Restore auto triggering
            self._scope.close()
            self._scope = None
