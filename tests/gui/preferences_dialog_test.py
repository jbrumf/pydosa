"""
Interactive test for preferences_dialog.

This allows the dialog to be exercised interactively.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import os
from configparser import ConfigParser
from tkinter import Tk

from pydosa.dsa.preferences_dialog import PreferencesDialog

# FIXME: Use a dedicated resources file for test data
PREFERENCES_FILE = os.path.expanduser('~/.pydosa.cfg')


def try_preferences():
    """Prompt with a preferences dialog and print results"""
    config = ConfigParser()
    config.read(PREFERENCES_FILE)

    root = Tk()
    ok = PreferencesDialog.ask(root, config)
    print(ok)
    print(config.sections())
    print(config.items('DEVICE'))


if __name__ == "__main__":
    try_preferences()
