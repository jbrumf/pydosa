"""
Main application GUI for the spectrum analyzer.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import sys
from tkinter import Frame, Button, Label, OptionMenu, StringVar, Menu
from tkinter import Tk
from tkinter import messagebox
from tkinter.constants import SUNKEN

from numpy import array as npa

import pydosa
from pydosa.dsa import instrument
from pydosa.dsa.analyzer import Analyzer
from pydosa.dsa.preferences_dialog import PreferencesDialog
from pydosa.dsa.scope_thread import ScopeThread
from pydosa.dsa.spectrum_plot import SpectrumPlot
from pydosa.sim.sim_driver import SimDriver
from pydosa.sim.wavegen import WaveGen
from pydosa.sim.wavegen_panel import WavegenPanel
from pydosa.util.preferences_manager import PreferencesManager
from pydosa.util.settable_option_menu import SettableOptionMenu

# Configuration files
DSA_CONFIG = '.pydosa.cfg'
RESOURCES = 'pydosa.data'

# Initial option settings
INITIAL_MODE = 'Normal'
INITIAL_WINDOW = 'Hanning'
DESELECTED_ITEM = '-'
INITIAL_FMAX = 100e6

# Option lists displayed in menus
MODES = ['Normal', 'Average', 'Maximum', 'Minimum']
WINDOWS = ['Rectangle', 'Hanning', 'Flat-Top', 'Blackman']


class DsaGui(object):
    """Application GUI"""

    def __init__(self, root):
        """Initialization"""
        root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root = root
        self.prefs = PreferencesManager(DSA_CONFIG, RESOURCES)
        self.window = INITIAL_WINDOW
        # self.units: str = INITIAL_UNIT
        self.mode: str = INITIAL_MODE
        self._infovar = None
        self._pause_button = None
        self.wavegen = None
        self.wavepane = None
        self.thread = None
        self.fstart: float = 0  # Initial minimum frequency (Hz)
        self.fstop: float = 1e8  # Initial maximum frequency (Hz))
        self.plotter = None
        self.nsamples: str = '0'
        self.srate: str = '0'
        self.sratebox = None
        self.srate_var = None
        self.samplesbox = None
        self.samples_var = None
        self.rbw_var = None

        self._running = False
        self.analyzer = Analyzer()
        self.create_gui(root)
        self.init_menus()

    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self, value: bool):
        self._running = value
        self.set_run_button(value)  # FIXME: Perhaps only if changed?

    # ---------- Application logic ----------

    def connect(self, driver) -> None:
        """Connect driver"""
        if driver is None:
            self.init_menus()
            return

        # Configure instrument-specific menus
        self.setup_srate_menu(driver.sample_rates, driver.initial_sample_rate)
        self.setup_samples_menu(driver.sample_sizes, driver.initial_sample_size)

        # Stop any existing driver
        self.running = False
        if self.thread is not None:
            self.thread.close()
            self.thread = None

        # Initialize with new driver
        try:
            self.thread = ScopeThread(driver)
            self.thread.start()
            self.running = True

        # This exception should not normally occur
        except Exception:
            self.running = False
            messagebox.showwarning('Error',
                                   'Cannot connect to instrument')

    def start_app(self) -> None:
        """Start application after event loop is started"""
        if self.thread is not None:
            self.running = True
        self.run_loop()

    def process_data(self, measurement: tuple[npa, float]) -> None:
        """Analyse sample data and plot spectrum."""
        if measurement is not None:
            wave, sample_rate = measurement
            if wave is None or len(wave) == 0:
                return
            self.root.update()

            # Compute the spectrum
            data, srate = self.analyzer.compute_spectrum(wave, sample_rate,
                                                         self.mode, self.window)
            self.root.update()

            # Update spectrum plot)
            # self.plotter.set_range(self.fstart, self.fstop)
            self.plotter.plot_spectrum(data, sample_rate)

            # Update info panel
            ns = len(wave)
            rbw = float(sample_rate) / ns
            self.rbw_var.set('{:.1f}'.format(rbw))
            self.root.update()

    def run_loop(self) -> None:
        if self.running:
            if self.thread.is_ready():
                measurement = self.thread.get_data(self.nsamples, self.srate)
                self.process_data(measurement)

        elif self.thread is None:
            # FIXME: No need to redraw unless there has been a change event
            self.plotter.clear(self.fstart, self.fstop)
            self.wavepane.pack_forget()
            self.root.update()
        self.root.after(10, self.run_loop)

    def close_driver(self) -> None:
        """Close the instrument driver."""
        if self.thread is not None:
            self.thread.close()
            self.thread = None

    def quit(self) -> None:
        """Quit the application"""
        self.running = False
        self.close_driver()
        self.prefs.save()
        self.root.quit()
        sys.exit()

    # ---------- User interface ----------

    def create_gui(self, parent: Tk) -> None:
        """Create the user interface"""

        # Menus
        menubar = Menu(parent)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="About Pydosa...", command=self.about_dialog)
        filemenu.add_separator()
        filemenu.add_command(label="Open instrument...", command=self.choose_instrument)
        filemenu.add_command(label="Open simulator", command=self.simulator)
        filemenu.add_command(label="Close connection", command=self.close_connection)
        filemenu.add_separator()
        filemenu.add_command(label="Preferences...", command=self.open_preferences)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        parent.config(menu=menubar)

        main_frame = Frame(parent)
        self.root.title("Pydosa Spectrum Analyser")
        main_frame.pack(side='left')

        # Frame for controls above the main plot
        upper_frame = Frame(main_frame, pady=5)
        upper_frame.pack()

        col = 0
        label = Label(upper_frame, text='Analysis:  ')
        label.grid(row=0, column=col)

        col += 1
        mode_var = StringVar()
        mode_var.set(INITIAL_MODE)
        modebox = OptionMenu(upper_frame, mode_var,
                             *MODES, command=self.mode_callback)
        modebox.grid(row=0, column=col)
        label = Label(upper_frame, text='Mode')
        label.grid(row=1, column=col)

        col += 1
        window_var = StringVar()
        window_var.set(INITIAL_WINDOW)
        windowbox = OptionMenu(upper_frame, window_var,
                               *WINDOWS, command=self.window_callback)
        windowbox.grid(row=0, column=col)
        label = Label(upper_frame, text='Window')
        label.grid(row=1, column=col)

        col += 1
        label = Label(upper_frame, text='    ')  # Space
        label.grid(row=0, column=col)

        col += 1
        samples_options = [' ']
        self.samples_var = StringVar()
        self.samples_var.set(' ')
        self.samplesbox = SettableOptionMenu(upper_frame, self.samples_var,
                                             *samples_options,
                                             command=self.samples_callback)
        self.samplesbox.grid(row=0, column=col)
        label = Label(upper_frame, text='Samples')
        label.grid(row=1, column=col)

        col += 1
        srate_options = [' ']
        self.srate_var = StringVar()
        self.srate_var.set(' ')
        self.sratebox = SettableOptionMenu(upper_frame, self.srate_var,
                                           *srate_options, command=self.srate_callback)
        self.sratebox.grid(row=0, column=col)
        label = Label(upper_frame, text='Sa/s')
        label.grid(row=1, column=col)

        col += 1
        label = Label(upper_frame, text='')  # Space
        label.grid(row=0, column=col)

        col += 1
        self.rbw_var = StringVar()
        self.rbw_var.set(' ')
        rbw_label = Label(upper_frame, textvariable=self.rbw_var,
                          relief=SUNKEN, width=6)
        rbw_label.grid(row=0, column=col)
        label = Label(upper_frame, text='RBW Hz')
        label.grid(row=1, column=col)

        col += 1
        label = Label(upper_frame, text='    ')  # Space
        label.grid(row=0, column=col)

        col += 1
        self._pause_button = Button(upper_frame, text="Pause", width=5,
                                    command=self.toggle_pause_callback)
        self._pause_button.grid(row=0, column=col)

        # Add the spectrum plot
        self.plotter = SpectrumPlot(main_frame, INITIAL_FMAX)

        # Status line
        self._infovar = StringVar()
        self._infovar.set(' ')
        info_label = Label(main_frame, textvariable=self._infovar,
                           relief=SUNKEN, width=100)
        info_label.pack(pady=5)

        # Simulator control panel
        sim_config = self.prefs.config['SIMULATOR']
        self.wavegen = WaveGen(sim_config)
        self.wavepane = WavegenPanel(self.root, self.wavegen)
        self.wavepane.pack_forget()

    # ---------- Menu re-configuration ----------

    def init_menus(self) -> None:
        """Initialize menus"""
        self.setup_srate_menu([DESELECTED_ITEM], DESELECTED_ITEM)
        self.setup_samples_menu([DESELECTED_ITEM], DESELECTED_ITEM)

    def setup_srate_menu(self, sample_rates: list[str], initial_rate: str) -> None:
        """Set up the sample rate menu."""
        self.sratebox.set_items(sample_rates)
        self.srate_var.set(initial_rate)
        self.srate_callback(initial_rate)

    def setup_samples_menu(self, sample_sizes: list[str], initial_size: str) -> None:
        """Set up the samples menu."""
        self.samplesbox.set_items(sample_sizes)
        self.samples_var.set(initial_size)
        self.samples_callback(initial_size)

    def show_message(self, message: str) -> None:
        """Display a message on the info line."""
        self._infovar.set(message)

    # ---------- GUI callbacks ----------

    def about_dialog(self) -> None:
        # Display the 'About' dialog
        messagebox.showinfo('About Pydosa',
                            'PYDOSA\n\n'
                            + 'Digital Oscilloscope Spectrum Analyzer\n'
                            + 'Version ' + pydosa.__version__ + '\n\n'
                            + 'Copyright (c) 2020 Jon Brumfitt\n'
                            + 'Licensed under MIT License',
                            parent=self.root)

    def open_preferences(self) -> None:
        """Open the preferences dialog"""
        self.running = False
        self.prefs.load()
        ok = PreferencesDialog.ask(self.root, self.prefs.config)
        if ok:
            self.prefs.save()
        self.running = True

    def choose_instrument(self) -> None:
        """Open the Choose Instrument dialog."""
        self.running = False
        self.close_driver()
        driver = instrument.choose_instrument(self.prefs, self.root)
        self.connect(driver)
        self.wavepane.pack_forget()

    def simulator(self) -> None:
        """Start simulator"""
        self.running = False
        self.close_driver()
        driver = SimDriver(self.wavegen)
        self.connect(driver)
        self.wavepane.pack()

    def close_connection(self) -> None:
        """Close the instrument connection."""
        self.running = False
        self.close_driver()
        self.setup_srate_menu([DESELECTED_ITEM], DESELECTED_ITEM)
        self.setup_samples_menu([DESELECTED_ITEM], DESELECTED_ITEM)

    def toggle_pause_callback(self):
        """Callback to toggle the pause state."""
        if self.thread is None:
            return
        self.running = not self.running

    def set_run_button(self, running: bool) -> None:
        """Set text on pause button to match run state"""
        if running:
            self._pause_button.config(text='Pause')
        else:
            self._pause_button.config(text='Run')

    def mode_callback(self, option: StringVar) -> None:
        """Callback to change the averaging mode"""
        self.mode = option

    def window_callback(self, option: StringVar) -> None:
        """Callback to change the FFT window function"""
        self.window = option

    def samples_callback(self, option: str) -> None:
        """Callback to change the number of samples"""
        if option == DESELECTED_ITEM:
            self.nsamples = '0'
        else:
            self.nsamples = option

    def srate_callback(self, option: str) -> None:
        """Callback to change the minimum sample rate"""
        if option == DESELECTED_ITEM:
            self.srate = '0'
        else:
            self.srate = option


def main():
    """Main program to launch the application"""
    root = Tk()
    gui = DsaGui(root)
    root.eval('tk::PlaceWindow . center')
    root.after(100, lambda: gui.start_app())
    root.mainloop()
    sys.exit()


if __name__ == "__main__":
    main()
