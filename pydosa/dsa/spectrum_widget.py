"""
GUI widget to display the spectrum.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import math
from tkinter import Canvas, N, W

import numpy as np

from pydosa.util import util, units

VDIVS = 14  # Vertical divisions
VSCALE = 40  # pixels / vertical division
VOFF = 20  # Margin at top (pixels)
HOFF = 35  # Horizontal offset
BORDER = 0
FTICKS = 10  # Preferred number of frequency tick marks

PLOT_WIDTH = 1024  # Width of plot (pixels) FIXME: TEMPORARY

TRACE_COLOR = "#FFFF30"
GRID_COLOR = "#606060"
AXIS_COLOR = "#B0B0B0"
TEXT_COLOR = "#FFFFFF"


class SpectrumWidget(Canvas):
    """GUI widget to display the spectrum."""

    def __init__(self, parent, width, height, info_handler=None):
        """Initialization"""

        # Old-style super call as Canvas is not a new-style class
        Canvas.__init__(self, parent, width=width, height=height,
                        background="black", borderwidth=BORDER,
                        relief='raised')
        self.pack(padx=10, pady=10)
        self.parent = parent
        self.info_handler = info_handler

        self.fmin = 0
        self.fmax = 1e7
        self.sample_rate = 1e9
        self.ntick = FTICKS
        self.dbscale = 10
        self.level = 0

    def set_range(self, fmin, fmax):
        """Set the frequency range."""
        self.fmin = fmin
        self.fmax = fmax

    def set_sample_rate(self, rate):
        """Set the sample rate."""
        self.sample_rate = rate

    def plot_spectrum(self, data):
        """Plot the spectrum"""

        width = PLOT_WIDTH  # X pixels
        nsamp = len(data)  # No. of FFT bins
        fmin = self.fmin
        fmax = self.fmax
        srate = float(self.sample_rate)

        # Rescale frequency data to required span
        dfpix = (fmax - fmin) / width  # df per pixel
        dfsamp = srate / 2 / (nsamp - 1)  # df per FFT bin
        imin = math.floor(fmin / dfsamp)
        imax = math.ceil(fmax / dfsamp)
        if imax >= nsamp:
            imax = nsamp - 1

        a = np.arange(imin, imax + 1)
        plotx = (a * dfsamp - fmin) / dfpix + HOFF
        ploty = data[imin:imax + 1] - self.level
        self.delete("all")
        self.draw_grid()

        size = len(plotx)  # Number of frequency bins in span
        ploty = ploty * (-VSCALE / self.dbscale) + VOFF  # Convert dB to pixels

        ka = (fmax-fmin)/srate * (2*nsamp)/width
        if self.info_handler:
            self.info_handler('Bins/pixel=%.2f' % ka)
        k = int(ka)

        # Rebin if #bins > #pixels
        if k > 0:
            n = size // k
            m = n * k
            plotx = plotx[0:m]
            ploty = ploty[0:m]
            xx = plotx.reshape(n, k)
            yy = ploty.reshape(n, k)
            plotx = xx.mean(1)  # Plotting will round this
            ploty = yy.min(1)  # Min pixel coordinate = Max power
            size = n

        # At least 2 points are needed for a plot
        if size >= 2:
            array = np.array([plotx, ploty]).reshape(size * 2, order='F')
            self.create_line(array.tolist(), fill=TRACE_COLOR)

    def draw_grid(self):
        """Draw the grid lines and label them"""

        # Draw horizontal grid lines
        for i in range(0, VDIVS + 1):
            y = VOFF + i * VSCALE
            line = [HOFF, y, HOFF + PLOT_WIDTH, y]
            self.create_line(line, fill=GRID_COLOR)
            label = str(-i * self.dbscale + self.level)
            self.create_text(3, y, text=label, anchor=W, fill=TEXT_COLOR)

        # Draw vertical grid lines
        (step, minx, maxx) = self.grid_scale(self.fmin, self.fmax)
        f = minx
        while f <= maxx:
            x = HOFF + self.freq_to_pixel(f)
            line = [x, VOFF, x, VOFF + VDIVS * VSCALE]
            self.create_line(line, fill=GRID_COLOR)
            # label = "%g" % f
            label = units.encode_metric_prefix(f)
            y = VOFF + VDIVS * VSCALE
            self.create_text(x, y + 3, text=label, anchor=N, fill=TEXT_COLOR)
            f = f + step

    def freq_to_pixel(self, freq):
        """Convert frequency to pixel offset."""
        width = PLOT_WIDTH
        fmin = self.fmin
        fmax = self.fmax
        dfpix = (fmax - fmin) / width

        return (freq - fmin) / dfpix

    def grid_scale(self, minv, maxv):
        """ Find nice round numbers for labelling the axes"""
        rng = util.ceil_nice_number(maxv - minv)
        step = util.round_nice_number(rng / (self.ntick - 1))
        min_value = math.floor(minv / step) * step
        max_value = math.ceil(maxv / step) * step

        return step, min_value, max_value
