#!/usr/bin/env python3
"""
Interactive command-line SCPI client.

Avoid commands that return binary data as these are not
handled correctly.

The host can be set using command-line options:
  --host <IP|hostname>

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import atexit
import getopt
import os
import readline  # Don't delete: Enables history
import sys

import vxi11

DEFAULT_HOST = "192.168.1.5"


def scpi(host):
    """Connect to device at specified host and port"""

    # Read history file if it exists
    histfile = os.path.join(os.environ["HOME"], ".scpihist")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)

    # Open a connection to the instrument
    instr = vxi11.Instrument(host)
    command = '*IDN?'
    print(instr.ask(command))

    try:
        while True:
            command = input("scpi> ").strip()
            print()
            if command.lower() == "exit":
                break
            if command.find('?') < 0:
                instr.write(command)
            else:
                print("[", command, "]")
                print(instr.ask(command))
    except EOFError:  # CNTL-D to exit
        pass
    print("Exit")
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
