"""
Enhanced OptionMenu.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
from tkinter import OptionMenu


class SettableOptionMenu(OptionMenu):
    """An OptionMenu that allows the item list to be replaced."""

    def __init__(self, master, variable, value, *values, **kwargs):
        super(SettableOptionMenu, self).__init__(master, variable, value, *values,
                                                 **kwargs)
        self.parent = super()
        self.variable = variable
        self.command = None
        if 'command' in kwargs:
            self.command = kwargs['command']

    def set_items(self, items: list[str]) -> None:
        """Replace the list of items"""
        menu = self['menu']
        menu.delete(0, 'end')
        for s in items:
            menu.add_command(label=s, command=lambda x=s: self.option_callback(x))

    def option_callback(self, option) -> None:
        """Callback to set the selected option."""
        self.variable.set(option)
        if self.command is not None:
            self.command(option)
