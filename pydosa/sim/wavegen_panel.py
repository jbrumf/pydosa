"""
GUI pane for controlling waveform generator.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
from tkinter import Frame, LabelFrame
from tkinter import Label, OptionMenu, StringVar, Entry
from tkinter.constants import W, E

TEXT_COLOR = "#000000"
INVALID_COLOR = "#FF0000"


class WavegenPanel(Frame):
    """GUI pane for controlling waveform generator."""

    def __init__(self, parent, wavegen):
        Frame.__init__(self, parent)
        self.parent = parent

        self.var_nsamples = None
        self.entry_nsamples = None
        self.entry_nsamples = None
        self.var_freq = None
        self.var_ampl = None
        self.entry_quant = None
        self.var_quant = None
        self.var_noise_units = None
        self.entry_noise = None
        self.var_noise = None
        self.entry_dc = None
        self.var_dc = None
        self.entry_amdepth = None
        self.var_amdepth = None
        self.entry_amfreq = None
        self.var_amfreq = None
        self.var_ampl_units = None
        self.entry_ampl = None
        self.entry_freq = None

        self.wavegen = wavegen
        self.config = wavegen.config
        self.create_gui(self)

    def create_gui(self, parent) -> None:
        """Create the user interface"""

        padx = 5
        pady = 4

        # ----- Sine wave -----

        label = Label(parent, text="Instrument simulator", font='Helvetica 16')
        label.pack(pady=(55, 0))  # FIXME: Avoid absolute dimensions

        row = 0
        frame1 = LabelFrame(parent, text='Sine Wave')
        frame1.pack(padx=15, pady=15, ipady=5)
        frame1.columnconfigure(0, minsize=80)

        # ----- Frequency -----
        row += 1
        label = Label(frame1, text="Frequency")
        label.grid(row=row, column=0, stick=E)

        self.var_freq = StringVar()
        self.var_freq.set(self.wavegen.freq)
        self.var_freq.trace("w", self.validate_frequency)
        self.entry_freq = Entry(frame1, textvariable=self.var_freq)
        self.entry_freq.grid(row=row, column=1, padx=padx, pady=pady)
        self.entry_freq.config(width=12)
        self.entry_freq.bind('<Return>', self.frequency_accept)
        self.entry_freq.bind('<FocusOut>', self.frequency_accept)

        label = Label(frame1, text="Hz")
        label.grid(row=row, column=2, stick=W, padx=padx)

        # ----- Amplitude -----
        row += 1

        label = Label(frame1, text="Amplitude")
        label.grid(row=row, column=0, stick=E)

        self.var_ampl = StringVar()
        self.var_ampl.set(self.wavegen.amplitude)
        self.var_ampl.trace("w", self.validate_amplitude)
        self.entry_ampl = Entry(frame1, textvariable=self.var_ampl)
        self.entry_ampl.grid(row=row, column=1, padx=padx, pady=pady)
        self.entry_ampl.config(width=12)
        self.entry_ampl.bind('<Return>', self.amplitude_accept)
        self.entry_ampl.bind('<FocusOut>', self.amplitude_accept)

        units_options = ['Vpk', 'Vrms', 'dBm']
        self.var_ampl_units = StringVar()
        self.var_ampl_units.set(self.wavegen.units)
        box_ampl_units = OptionMenu(frame1, self.var_ampl_units, *units_options,
                                    command=self.amplitude_units)
        box_ampl_units.configure(width=4)
        box_ampl_units.grid(row=row, column=2, padx=padx)

        # ----- AM modulation frequency -----
        row += 1

        label = Label(frame1, text="AM freq")
        label.grid(row=row, column=0, stick=E)

        self.var_amfreq = StringVar()
        self.var_amfreq.set(self.wavegen.mod_freq)
        self.var_amfreq.trace("w", self.validate_amfreq)
        self.entry_amfreq = Entry(frame1, textvariable=self.var_amfreq)
        self.entry_amfreq.grid(row=row, column=1, padx=padx, pady=pady)
        self.entry_amfreq.config(width=12)
        self.entry_amfreq.bind('<Return>', self.amfreq_accept)
        self.entry_amfreq.bind('<FocusOut>', self.amfreq_accept)

        label = Label(frame1, text="Hz")
        label.grid(row=row, column=2, stick=W, padx=padx)

        # ----- AM modulation depth -----
        row += 1

        label = Label(frame1, text="Mod depth")
        label.grid(row=row, column=0, stick=E)

        self.var_amdepth = StringVar()
        self.var_amdepth.set(self.wavegen.mod_depth)
        self.var_amdepth.trace("w", self.validate_amdepth)
        self.entry_amdepth = Entry(frame1, textvariable=self.var_amdepth)
        self.entry_amdepth.grid(row=row, column=1, padx=padx, pady=pady)
        self.entry_amdepth.config(width=12)
        self.entry_amdepth.bind('<Return>', self.amdepth_accept)
        self.entry_amdepth.bind('<FocusOut>', self.amdepth_accept)

        label = Label(frame1, text="%")
        label.grid(row=row, column=2, stick=W, padx=padx)

        # ---------- Lower frame ----------

        frame2 = LabelFrame(parent, text='General')
        frame2.pack(padx=15, pady=10)
        frame2.columnconfigure(0, minsize=80)
        # frame2.rowconfigure(0, minsize=100)

        # ----- DC level -----
        row += 1

        label = Label(frame2, text="DC offset")
        label.grid(row=row, column=0, stick=E)

        self.var_dc = StringVar()
        self.var_dc.set(self.wavegen.dc)
        self.var_dc.trace("w", self.validate_dc)
        self.entry_dc = Entry(frame2, textvariable=self.var_dc)
        self.entry_dc.grid(row=row, column=1, padx=padx, pady=pady)
        self.entry_dc.config(width=12)
        self.entry_dc.bind('<Return>', self.dc_accept)
        self.entry_dc.bind('<FocusOut>', self.dc_accept)

        label = Label(frame2, text="V")
        label.grid(row=row, column=2, stick=W, padx=padx)

        # ----- Noise -----
        row += 1

        label = Label(frame2, text="Noise")
        label.grid(row=row, column=0, stick=E)

        self.var_noise = StringVar()
        self.var_noise.set(self.wavegen.noise)
        self.var_noise.trace("w", self.validate_noise)
        self.entry_noise = Entry(frame2, textvariable=self.var_noise)
        self.entry_noise.grid(row=row, column=1, padx=padx)
        self.entry_noise.config(width=12)
        self.entry_noise.bind('<Return>', self.noise_accept)
        self.entry_noise.bind('<FocusOut>', self.noise_accept)

        noise_units_options = ['Vrms', 'dBm']
        self.var_noise_units = StringVar()
        self.var_noise_units.set(self.wavegen.noise_units)
        box_noise_units = OptionMenu(frame2, self.var_noise_units, *noise_units_options,
                                     command=self.noise_units)
        box_noise_units.configure(width=4)
        box_noise_units.grid(row=row, column=2, padx=padx)

        # ----- Quantization -----
        row += 1

        label = Label(frame2, text="Quantize")
        label.grid(row=row, column=0, stick=E)

        self.var_quant = StringVar()
        self.var_quant.set(self.wavegen.quantization)
        self.var_quant.trace("w", self.validate_quantization)
        self.entry_quant = Entry(frame2, textvariable=self.var_quant)
        self.entry_quant.grid(row=row, column=1, padx=padx, pady=pady)
        self.entry_quant.config(width=12)
        self.entry_quant.bind('<Return>', self.quantization_accept)
        self.entry_quant.bind('<FocusOut>', self.quantization_accept)

        label = Label(frame2, text="V/level")
        label.grid(row=row, column=2, stick=W, padx=padx)

    # ----- Frequency callbacks -----

    def frequency_accept(self, arg) -> None:
        """Callback for change of frequency."""
        value = self.validate_frequency()
        if value is not None:
            self.wavegen.freq = value
            self.config['freq'] = value

    def validate_frequency(self, *arg) -> float | None:
        """Highlight the frequency if the value is invalid."""
        try:
            var = self.var_freq.get()
            value = float(var)
            if value <= 0:
                raise ValueError()
            self.entry_freq.config(fg=TEXT_COLOR)
            print(type(var))
            return var
        except ValueError:
            self.entry_freq.config(fg=INVALID_COLOR)
            return None

    # ----- Amplitude callbacks -----

    def amplitude_accept(self, arg) -> None:
        """Callback for change of amplitude."""
        value = self.validate_amplitude()
        if value is not None:
            self.wavegen.amplitude = value
            self.config['amplitude'] = value

    def validate_amplitude(self, *arg) -> float | None:
        """Highlight the amplitude if the value is invalid."""
        try:
            var = self.var_ampl.get()
            value = float(var)
            self.entry_ampl.config(fg=TEXT_COLOR)
            return var
        except ValueError:
            self.entry_ampl.config(fg=INVALID_COLOR)
            return None

    def amplitude_units(self, option) -> None:
        """Callback to change the amplitude units"""
        self.amplitude_accept(option)
        units = self.var_ampl_units.get()
        self.wavegen.units = units
        self.config['units'] = units

    # ----- AM frequency -----

    def amfreq_accept(self, arg) -> None:
        """Callback to change the AM modulation frequency"""
        value = self.validate_amfreq()
        if value is not None:
            self.wavegen.mod_freq = value
            self.config['mod_freq'] = value

    def validate_amfreq(self, *arg) -> float | None:
        """Highlight the AM frequency if the value is invalid."""
        try:
            var = self.var_amfreq.get()
            value = float(var)
            self.entry_amfreq.config(fg=TEXT_COLOR)
            return var
        except ValueError:
            self.entry_amfreq.config(fg=INVALID_COLOR)
            return None

    # ----- AM mod depth -----

    def amdepth_accept(self, arg) -> None:
        """Callback to change the AM modulation depth"""
        value = self.validate_amdepth()
        if value is not None:
            self.wavegen.mod_depth = value
            self.config['mod_depth'] = value

    def validate_amdepth(self, *arg) -> float | None:
        """Highlight the AM modulation depth if the value is invalid."""
        try:
            var = self.var_amdepth.get()
            value = float(var)
            self.entry_amdepth.config(fg=TEXT_COLOR)
            return var
        except ValueError:
            self.entry_amdepth.config(fg=INVALID_COLOR)
            return None

    # ----- Number of samples -----

    def nsamples_accept(self, arg) -> None:
        """Callback to change the number of samples"""
        value = self.validate_nsamples()
        if value is not None:
            self.wavegen.nsamples = value
            self.config['nsamples'] = value

    def validate_nsamples(self, *arg) -> float | None:
        """Highlight the number of samples if the value is invalid."""
        try:
            var = self.var_nsamples.get()
            value = int(var)
            self.entry_nsamples.config(fg=TEXT_COLOR)
            return var
        except ValueError:
            self.entry_nsamples.config(fg=INVALID_COLOR)
            return None

    # ----- DC offset -----

    def dc_accept(self, arg) -> None:
        """Callback to change the DC offset"""
        value = self.validate_dc()
        if value is not None:
            self.wavegen.dc = value
            self.config['dc'] = value

    def validate_dc(self, *arg) -> float | None:
        """Highlight the DC offset if the value is invalid."""
        try:
            var = self.var_dc.get()
            value = float(var)
            self.entry_dc.config(fg=TEXT_COLOR)
            return var
        except ValueError:
            self.entry_dc.config(fg=INVALID_COLOR)
            return None

    # ----- Noise -----

    def noise_accept(self, arg) -> None:
        """Callback to change the noise amplitude"""
        value = self.validate_noise()
        if value is not None:
            self.wavegen.noise = value
            self.config['noise'] = value

    def validate_noise(self, *arg) -> float | None:
        """Highlight the noise amplitude if the value is invalid."""
        try:
            var = self.var_noise.get()
            value = float(var)
            self.entry_noise.config(fg=TEXT_COLOR)
            return var
        except ValueError:
            self.entry_noise.config(fg=INVALID_COLOR)
            return None

    def noise_units(self, option) -> None:
        """Callback to change the noise units"""
        self.noise_accept(option)
        units = self.var_noise_units.get()
        self.wavegen.noise_units = units
        self.config['noise_units'] = units

    # ----- Quantization -----

    def quantization_accept(self, arg) -> None:
        """Callback to change the quantization"""
        value = self.validate_quantization()
        if value is not None:
            self.wavegen.quantization = value
            self.config['quantization'] = value

    def validate_quantization(self, *arg) -> float | None:
        """Highlight the quantization if the value is invalid."""
        try:
            var = self.var_quant.get()
            value = float(var)
            self.entry_quant.config(fg=TEXT_COLOR)
            return var
        except ValueError:
            self.entry_quant.config(fg=INVALID_COLOR)
            return None

    # ----- End of callbacks -----
