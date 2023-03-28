"""
Logger for VXI-11 connection for debugging use.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2023 Jon Brumfitt
"""

from pydosa.util.util import elide_bytes


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
        raw = self.instrument.read_raw()
        log('  read_raw ->', len(raw), 'bytes')
        # Check for IEEE definite-length block
        if b'#' in raw[0:15]:
            log('  ', elide_bytes(raw, 20, 3))
        else:
            log('  read_raw ->', len(raw), 'bytes')
        return raw

    def close(self):
        """Close the instrument connection"""
        self.instrument.close()
