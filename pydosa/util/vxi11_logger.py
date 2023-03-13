"""
Logger for VXI-11 connection for debugging use.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2023 Jon Brumfitt
"""


def log(*args):
    """Log a message"""
    msg = ' '.join([str(a) for a in args])
    print(msg)


class VxiLogger:
    """Logging wrapper for VXI-11 connection"""

    def __init__(self, instrument):
        self.instrument = instrument

    def ask(self, scpi: str) -> str:
        """Send SCPI query and return the result"""
        result = self.instrument.ask(scpi)
        log('SCPI', scpi, '\n  ->', result)
        return result

    def write(self, scpi: str):
        """Send a SCPI command"""
        log('SCPI', scpi)
        self.instrument.write(scpi)

    def read_raw(self) -> bytes:
        """Read and return raw bytes"""
        result = self.instrument.read_raw()
        log('  read_raw ->', len(result), 'bytes')
        return result

    def close(self):
        """Close the instrument connection"""
        self.instrument.close()
