"""
Manager for preferences files.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import importlib.resources as ilres
import os
from configparser import ConfigParser


class PreferencesManager(object):
    """Manager for preferences files."""

    def __init__(self, filename, resource_pkg):
        """Initialization"""
        self.filename = filename
        self.resource_pkg = resource_pkg
        self.preferences_file = os.path.expanduser('~/' + self.filename)
        self.resource = ilres.path(self.resource_pkg, self.filename)
        self.config = ConfigParser()  # Access ConfigParser here
        self._load_preferences()

    def _load_preferences(self):
        """Load the user preferences"""

        # Load the defaults
        with self.resource as tmp:
            defaults = self.config.read(tmp)
            self._log('Loading defaults: {}'.format(defaults))

        # Merge with user preferences if they exist
        prefs = self.config.read(self.preferences_file)
        self._log('Loading settings: {}'.format(prefs))

        # Save merged result as user preferences
        with open(self.preferences_file, 'w') as configfile:
            self.config.write(configfile)

    def load(self):
        """Load the user preferences file."""
        self.config.read(self.preferences_file)

    def save(self):
        """Save the preferences to the user preferences file."""
        with open(self.preferences_file, 'w') as configfile:
            self.config.write(configfile)

    def _log(self, message):
        print(message)
