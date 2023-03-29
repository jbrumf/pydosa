#!/usr/bin/env python3
"""
Interactive command-line SCPI client.

Replies with '#' in the first 15 bytes are assumed to be IEEE
binary blocks and are printed as bytes instead of ASCII.

The host can be set using the command-line option:
  -s <IP|hostname>

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import atexit
import getopt
import os
import readline  # Don't delete: Enables history
import sys

import vxi11

from pydosa.util.util import elide_bytes

DEFAULT_HOST = "192.168.1.5"
ENCODING = 'utf-8'
START_BYTES = 20  # Maximum start bytes in elided byte string
END_BYTES = 3  # Maximum end bytes in elided byte string


def scpi(host):
    """Connect to device at specified host"""

    # Read history file if it exists
    histfile = os.path.join(os.environ["HOME"], ".scpihist")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)

    # Open a connection to the instrument
    instr = vxi11.Instrument(host)
    print(instr.ask('*IDN?'))

    try:
        while True:
            command = input("scpi> ").strip()
            if command.lower() == "exit":
                break
            if command.find('?') < 0:
                instr.write(command)
            else:
                instr.write(command)
                reply = instr.read_raw()
                # Check for IEEE definite-length block
                if b'#' in reply[0:15]:
                    print(elide_bytes(reply, START_BYTES, END_BYTES))
                else:
                    print(reply.decode(ENCODING).rstrip('\r\n'))
            print()

    except EOFError:  # CNTL-D to exit
        pass
    instr.close()


def usage():
    """Print a command-line usage message"""
    print(sys.argv[0] + " [-s server]")


def main():
    """Main program to run from command line"""
    server = DEFAULT_HOST
    try:
        opts, arg = getopt.getopt(sys.argv[1:], "hs:", ["help", "server="])
        print(sys.argv)
        for opt, arg in opts:
            if opt in ("-s", "--server"):
                server = arg
            else:
                usage()
                sys.exit()
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    scpi(server)


if __name__ == "__main__":
    main()
