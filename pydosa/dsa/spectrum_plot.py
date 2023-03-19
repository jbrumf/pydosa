"""
Spectrum plot widget with integral view controls.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

from tkinter import Frame, OptionMenu, StringVar, Label

from numpy import array as npa

from pydosa.dsa.frequency_widget import FrequencyWidget
from pydosa.dsa.spectrum_widget import SpectrumWidget

# Initial option settings
INITIAL_DBSCALE = '10'  # dB/div
INITIAL_LEVEL = '0'  # Reference level
INITIAL_UNIT = 'dBm'
INITIAL_FMAX = 100e6  # Default maximum frequency

# Option lists displayed in menus
UNITS = ['dBm', 'dBV', 'dBc']
DBSCALES = ['1', '3', '5', '10', '15', '20']
LEVELS = ['30', '20', '10', '5', '0', '-5', '-10', '-20',
          '-30', '-40', '-50', '-60', '-70', '-80', '-90']


class SpectrumPlot(Frame):
    def __init__(self, parent, fmax: float = INITIAL_FMAX):
        Frame.__init__(self, parent)
        self.pack()
        self.parent = parent
        self.widget = None
        self.create_gui(fmax)

    def create_gui(self, fmax: float) -> None:
        main_frame = self

        self.widget = SpectrumWidget(main_frame, self.show_message)
        self.widget.set_range(0, fmax)
        self.widget.pack()

        button_frame = Frame(main_frame, pady=5)
        button_frame.pack()

        col = 0
        label = Label(button_frame, text='Frequency:  ')
        label.grid(row=0, column=col)

        col += 1
        freq_widget = FrequencyWidget(button_frame, self.freq_callback, 0, fmax)
        freq_widget.grid(row=0, column=col)

        col += 1
        label = Label(button_frame, text='       Scale:  ')  # Space
        label.grid(row=0, column=col)

        col += 1
        unit_var = StringVar()
        unit_var.set(INITIAL_UNIT)
        unitbox = OptionMenu(button_frame, unit_var,
                             *UNITS, command=self.unit_callback)
        unitbox.grid(row=0, column=col)
        label = Label(button_frame, text='Units')
        label.grid(row=1, column=col)

        col += 1
        dbscale_var = StringVar()
        dbscale_var.set(INITIAL_DBSCALE)
        dbscalebox = OptionMenu(button_frame, dbscale_var,
                                *DBSCALES, command=self.dbscale_callback)
        dbscalebox.grid(row=0, column=col)
        label = Label(button_frame, text='dB/div')
        label.grid(row=1, column=col)

        col += 1
        level_var = StringVar()
        level_var.set(INITIAL_LEVEL)
        levelbox = OptionMenu(button_frame, level_var,
                              *LEVELS, command=self.level_callback)
        levelbox.grid(row=0, column=col)
        label = Label(button_frame, text='Ref')
        label.grid(row=1, column=col)

    def clear(self, start: float, stop: float) -> None:
        """Clear spectrum, just leaving grid"""
        self.widget.clear(start, stop)

    def set_range(self, fstart: float, fstop: float) -> None:
        """Set the frequency range."""
        self.widget.set_range(fstart, fstop)

    def plot_spectrum(self, spectrum: npa, srate: float) -> None:
        """Plot a spectrum"""
        self.widget.plot_spectrum(spectrum, srate)

    def freq_callback(self, fstart: float, fstop: float) -> None:
        """Callback to change the frequency range."""
        self.widget.set_range(fstart, fstop)

    def unit_callback(self, option: StringVar) -> None:
        """Callback to change the units"""
        self.widget.units = option

    def dbscale_callback(self, option) -> None:
        """Callback to change the decibel scale"""
        self.widget.dbscale = int(option)

    def level_callback(self, option) -> None:
        """Callback to change the reference level"""
        self.widget.level = int(option)

    def show_message(self, message: str) -> None:
        # print(message)
        pass
