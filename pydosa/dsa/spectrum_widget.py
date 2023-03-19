"""
GUI widget to display the spectrum.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import math
from tkinter import Canvas, N, W

import numpy as np
from numpy import array as npa

from pydosa.util import units, util

# Window geometry
PLOT_WIDTH = 1024  # Pixels
PLOT_HEIGHT = 620  # Pixels
PLOT_MARGIN = 30  # Pixels

# Geometry
VDIVS = 14  # Vertical divisions
VSCALE = 40  # pixels / vertical division
VOFF = 20  # Margin at top (pixels)
HOFF = 35  # Horizontal offset
BORDER = 0
FTICKS = 10  # Preferred number of frequency tick marks

# Colours
TRACE_COLOR = "#FFFF30"
GRID_COLOR = "#606060"
AXIS_COLOR = "#B0B0B0"
TEXT_COLOR = "#FFFFFF"

# Constants
DB3 = 10 * math.log10(2)  # 3 dB


class SpectrumWidget(Canvas):
    """GUI widget to display the spectrum."""

    # def __init__(self, parent, width, height, info_handler=None):
    def __init__(self, parent, info_handler=None):
        """Initialization"""
        width = PLOT_WIDTH + 2 * PLOT_MARGIN

        # Old-style super call as Canvas is not a new-style class
        Canvas.__init__(self, parent, width=width, height=PLOT_HEIGHT,
                        background="black", borderwidth=BORDER,
                        relief='raised')
        self.pack(padx=10, pady=10)
        self.parent = parent
        self.info_handler = info_handler

        self.fmin = 0
        self.fmax = 0
        self.sample_rate = 0
        self.ntick = FTICKS
        self.dbscale = 10
        self.level = 0
        self.units = 'dBm'

    def set_range(self, fmin: float, fmax: float) -> None:
        """Set the frequency range."""
        self.fmin = fmin
        self.fmax = fmax

    def clear(self, fstart: float, fstop: float) -> None:
        """Clear spectrum, just leaving grid"""
        self.set_range(fstart, fstop)
        self.delete("all")
        self.draw_grid()

    def plot_spectrum(self, data: npa, srate: float) -> None:
        """Plot the spectrum (data in dBV)"""
        width = PLOT_WIDTH  # X pixels
        nsamp = len(data)  # No. of FFT bins
        fmin = self.fmin
        fmax = self.fmax

        # Scale to required units
        offset_db = 0
        match self.units:
            case 'dBV':  # RMS
                pass
            case 'dBm':
                offset_db += 10 + DB3  # 1V RMS in 50R = 13.01 dBm
            case 'dBc':
                offset_db = -max(data)
            case _:
                raise ValueError("Unknown unit: ", self.units)
        if offset_db != 0:
            data += offset_db

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

        ka = (fmax - fmin) / srate * (2 * nsamp) / width
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

    def draw_grid(self) -> None:
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

    def freq_to_pixel(self, freq: float) -> float:
        """Convert frequency to pixel offset."""
        width = PLOT_WIDTH
        fmin = self.fmin
        fmax = self.fmax
        dfpix = (fmax - fmin) / width

        return (freq - fmin) / dfpix

    def grid_scale(self, minv: float, maxv: float) -> tuple[float, float, float]:
        """ Find nice round numbers for labelling the axes"""
        rng = util.ceil_nice_number(maxv - minv)
        step = util.round_nice_number(rng / (self.ntick - 1))
        min_value = math.floor(minv / step) * step
        max_value = math.ceil(maxv / step) * step

        return step, min_value, max_value
