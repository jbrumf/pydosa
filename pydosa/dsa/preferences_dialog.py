"""
GUI dialog for entering spectrum analyzer preferences.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
from configparser import ConfigParser
from tkinter import Entry, StringVar, Label, Frame

from pydosa.util.modal_dialog import ModalDialog

TEXT_COLOR = "#000000"
INVALID_COLOR = "#FF0000"


class PreferencesDialog(ModalDialog):
    """GUI dialog for entering spectrum analyzer preferences."""

    @classmethod
    def ask(cls, parent, config: ConfigParser) -> bool:
        """Show the dialog and return updated preferences."""
        dialog = PreferencesDialog(parent, config)
        return dialog.result

    def __init__(self, parent, config: ConfigParser):
        """Initialization"""
        self.config = config
        if not config.has_section('DEVICE'):
            config.add_section('DEVICE')
        device = config['DEVICE']

        self.server = device.get('server')
        self.v1 = None
        self.e1 = None
        # self.plugins = device.get('plugins')
        # self.v2 = None
        # self.e2 = None

        self.result = False
        ModalDialog.__init__(self, parent, 'Preferences')

    def create_content(self, master: Frame) -> None:
        """Create the dialog widgets."""
        self.v1 = StringVar()
        self.v1.set(self.server)
        label = Label(master, text='Server')
        label.grid(row=0, column=0)
        self.e1 = Entry(master, textvariable=self.v1)
        self.e1.grid(row=0, column=1)

        # self.v2 = StringVar()
        # self.v2.set(self.plugins)
        # label = Label(master, text='Plugins')
        # label.grid(row=1, column=0)
        # self.e2 = Entry(master, textvariable=self.v2)
        # self.e2.grid(row=1, column=1)

    def ok_action(self) -> None:
        """Callback for press of OK button"""
        try:
            device = self.config['DEVICE']
            device['server'] = self.v1.get()
            # device['plugins'] = self.v2.get()
            self.result = True
        except Exception as e:
            print(e)
        pass
