#!/usr/bin/env python3
"""
Software spectrum analyser for the Siglent SDS1xx4X-E oscilloscope.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

from pydosa.tools import scpi_client

# Options: [--server=server] [--port=port] [--help]
if __name__ == "__main__":
    scpi_client.main()
