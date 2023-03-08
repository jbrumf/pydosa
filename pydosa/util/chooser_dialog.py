"""
GUI dialog for choosing items.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
from tkinter import Label, OptionMenu, StringVar

from pydosa.util.modal_dialog import ModalDialog

TEXT_COLOR = "#000000"
INVALID_COLOR = "#FF0000"


class ChooserDialog(ModalDialog):
    """GUI dialog for choosing an item."""

    @classmethod
    def ask(cls, parent, items, title='Choose item', message=None):
        """Show the dialog and return updated preferences."""
        dialog = ChooserDialog(parent, items, title, message)
        return dialog.result

    def __init__(self, parent, items, title, message):
        """Initialization"""
        self.items = items
        self.message = message
        self.item_var = None
        self.result = None
        ModalDialog.__init__(self, parent, title)

    def create_content(self, master):
        """Create the dialog widgets."""
        label = Label(master, text=self.message)
        label.pack()
        options = self.items
        self.item_var = StringVar()
        self.item_var.set(self.items[0])
        itembox = OptionMenu(master, self.item_var, *options)
        itembox.pack()

    def ok_action(self):
        """Callback for press of OK button"""
        try:
            self.result = self.item_var.get()
        except Exception as e:
            print(e)
        pass
