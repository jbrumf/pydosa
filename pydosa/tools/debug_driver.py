"""To debug prototype driver.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt"""

import math

import vxi11

# Replace the next line with import of the prototype driver
from pydosa.plugins.siglent_sds1000xe import Driver
from pydosa.util.units import decode_unit_prefix
from pydosa.util.vxi11_logger import VxiLogger

HOST = '192.168.1.5'  # IP address of your scope
NSAMPLES = 1024  # Number of waveform samples requested
SRATE = '1G'  # Sampling rate requested


def main():
    # Connect to the instrument and log the SCPI commands
    instr = vxi11.Instrument(HOST)
    instr = VxiLogger(instr)

    # Instantiate the driver and request some samples
    driver = Driver()
    driver.open(instr)
    driver.prepare()
    data, srate = driver.fetch_data(NSAMPLES, SRATE)

    # Print the response
    print('\ndata=', data)
    print('length=', len(data), ', srate=', srate)

    # Check that the actual nsamples and srate match those requested
    assert len(data) == NSAMPLES
    assert (math.fabs(decode_unit_prefix(SRATE) - srate) < 0.01)

    # Close the driver which will close the connection
    driver.close()


if __name__ == '__main__':
    main()
