"""
GUI widget for entering a frequency range.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
from tkinter import Frame, StringVar, Entry, OptionMenu
from tkinter.constants import LEFT

MIN_FREQ = 0  # Initial minimum frequency (Hz)
MAX_FREQ = 1E8  # Initial maximum frequency (Hz)
MAXIMUM = 5E8  # Maximum allowed frequency
MIN_SPAN = 10  # Minimum span (Hz)

ENTRY_WIDTH = 9  # Width of Entry fields

UNITS_DICT = {'MHz': 1e6, 'kHz': 1e3, 'Hz': 1}

TEXT_COLOR = "#000000"
INVALID_COLOR = "#FF0000"


class FrequencyWidget(Frame):
    """GUI widget for entering a frequency range."""

    def __init__(self, parent, callback=None, fmin: float = MIN_FREQ, fmax: float = MAX_FREQ):
        """Initialization - Create the widget"""
        self.scale = 1e6

        Frame.__init__(self, parent)
        self.parent = parent
        self.callback = callback
        self.fmin = fmin
        self.fmax = fmax

        mode_options = ['Min/Max', 'Centre/Span']
        self.mode = mode_options[0]
        self.mode_var = StringVar(self)
        self.mode_var.set(self.mode)
        self.modebox = OptionMenu(self, self.mode_var, *mode_options,
                                  command=self.mode_callback)
        # self.modebox.config(width=10)
        self.modebox.pack(side=LEFT)

        # First numeric entry field
        self.var1 = StringVar()
        self.var1.set(repr(self.fmin / self.scale))
        self.var1.trace("w", self.changed)
        self.entry1 = Entry(self, textvariable=self.var1)
        self.entry1.config(width=ENTRY_WIDTH)
        self.entry1.bind('<Return>', self.accept_callback)
        self.entry1.bind('<FocusOut>', self.accept_callback)
        self.entry1.pack(side=LEFT)

        # Second numeric entry field
        self.var2 = StringVar()
        self.var2.set(repr(self.fmax / self.scale))
        self.var2.trace("w", self.changed)
        self.entry2 = Entry(self, textvariable=self.var2)
        self.entry2.config(width=ENTRY_WIDTH)
        self.entry2.bind('<Return>', self.accept_callback)
        self.entry2.bind('<FocusOut>', self.accept_callback)
        self.entry2.pack(side=LEFT)

        units_options = ['MHz', 'kHz', 'Hz']
        self.units = units_options[0]
        self.units_var = StringVar(self)
        self.units_var.set(self.units)
        self.unitsbox = OptionMenu(self, self.units_var, *units_options,
                                   command=self.units_callback)
        # self.unitsbox.config(width=3)
        self.unitsbox.pack(side=LEFT)

    def units_callback(self, option) -> None:
        """Callback to change frequency units"""
        scale = UNITS_DICT[option]

        if scale != self.scale:
            try:
                fmin = float(self.var1.get()) * self.scale
                fmax = float(self.var2.get()) * self.scale
                self.var1.set(str(fmin / scale))
                self.var2.set(str(fmax / scale))
            except Exception:
                pass
            self.scale = scale
            self.changed(None)

    def mode_callback(self, option) -> None:
        """Callback for mode option menu (Min/Max or Centre/Span)"""
        mode = self.mode_var.get()
        if mode == self.mode:  # Ignore if mode hasn't changed
            return

        old_mode = self.mode
        self.mode = mode  # Needed by validate method

        try:
            if mode == 'Centre/Span':
                fmin = float(self.var1.get()) * self.scale
                fmax = float(self.var2.get()) * self.scale
                centre = (fmin + fmax) / 2
                span = fmax - fmin
                self.var1.set(str(centre / self.scale))
                self.var2.set(str(span / self.scale))
                self.fmin = fmin
                self.fmax = fmax
            else:
                centre = float(self.var1.get()) * self.scale
                span = float(self.var2.get()) * self.scale
                fmin = centre - span / 2
                fmax = centre + span / 2
                self.var1.set(str(fmin / self.scale))
                self.var2.set(str(fmax / self.scale))
                self.fmin = fmin
                self.fmax = fmax

        except ValueError:
            # Don't allow mode change while numbers are invalid
            self.mode = old_mode
            self.mode_var.set(old_mode)

    # Something changed in one of the entry fields

    def changed(self, *arg) -> None:
        """Highlight invalid entries"""
        ok, fmin, fmax = self.validate()
        if ok:
            self.entry1.config(fg=TEXT_COLOR)
            self.entry2.config(fg=TEXT_COLOR)
        else:
            self.entry1.config(fg=INVALID_COLOR)
            self.entry2.config(fg=INVALID_COLOR)

    def validate(self) -> tuple[bool, float, float]:
        """Parse and validate the entry fields"""
        fmin = self.fmin
        fmax = self.fmax
        valid = True

        if self.mode == 'Centre/Span':
            try:
                centre = float(self.var1.get()) * self.scale
                span = float(self.var2.get()) * self.scale
                fmin = centre - span / 2
                fmax = centre + span / 2
            except Exception:
                valid = False
        else:
            try:
                fmin = float(self.var1.get()) * self.scale
                fmax = float(self.var2.get()) * self.scale
            except Exception:
                valid = False

        if fmin < 0 or fmin > MAXIMUM or fmax < 0 \
                or fmax > MAXIMUM or fmax - fmin < MIN_SPAN:
            valid = False

        return valid, fmin, fmax  # Ignore fmin/fmax if not valid

    def accept_callback(self, event) -> None:
        """Called when Enter/Return key pressed in one of the
           entry fields or focus is lost"""
        ok, fmin, fmax = self.validate()

        if ok and self.callback is not None:
            self.fmin = fmin
            self.fmax = fmax
            # print("ok: " + repr(fmin) + " " + repr(fmax))
            self.callback(fmin, fmax)
