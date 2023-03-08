"""
Thread wrapper for a scope driver.

Running the scope driver in a thread allows it to acquire and retrieve
the next set of samples whilst the main thread is analysing and
displaying the previous set of samples. The driver can enter a
wait-loop whilst waiting for a data acquisition complete.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

import threading
import time
from pydosa.util.units import decode_unit_prefix
from pydosa.dsa.scope_driver import ScopeDriver

lock = threading.Lock()


class ScopeThread(threading.Thread):

    def __init__(self, driver):
        threading.Thread.__init__(self)
        self.driver: ScopeDriver = driver
        self.driver.prepare()
        self.data = None  # (samples, sara)
        self.ready = False
        self.stop = False
        self.srate_option = '1G'
        self.nsamples_option = '1Mi'

    def run(self):
        while not self.stop:
            while self.is_ready():
                if self.stop:
                    return
                time.sleep(0.01)
            nsamples = int(decode_unit_prefix(self.nsamples_option))
            data = self.driver.fetch_data(nsamples, self.srate_option)
            with lock:
                self.data = data  # Make the data available

    def get_data(self, nsamples_option, srate_option):
        """Called from main thread to get next set of data.
           nsamples & srate apply to the next acquisition.
        """
        with lock:
            # Set parameters for next acquisition
            self.nsamples_option = nsamples_option
            self.srate_option = srate_option
            data = self.data
            self.data = None
            return data

    def is_ready(self):
        """Return True if data is ready."""
        with lock:
            return self.data is not None

    def close(self):
        """Interrupt the thread."""
        self.stop = True
