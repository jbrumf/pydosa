"""
Calculates element-wise average/min/max.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

import numpy as np
from numpy import array as npa


class Averager(object):
    """Calculates element-wise average/min/max"""

    def __init__(self, alpha):
        """Initialization"""
        self._average = None
        self._alpha = alpha
        self._count = 0  # Averaging count
        self._last_mode = None
        self._monitor = None

    def reset(self) -> None:
        """Reset the averager and release storage"""
        self._average = None
        self._count = 0  # Averaging count
        self._last_mode = None

    def average(self, data: npa, mode, monitor=None) -> npa:
        """Calculate element-wise average/min/max.
           Averaging is reset if the value of monitor changes."""

        # Reset averaging if it becomes invalidated
        if (mode != self._last_mode) \
                or (monitor != self._monitor):
            self.reset()
            self._monitor = monitor
            self._last_mode = mode
            self._count = 0

        if self._average is None:
            self._average = np.array(data)  # Clone array
        else:
            match mode:
                case 'Normal':
                    pass
                case 'Maximum':
                    self._average = np.maximum(self._average, data)
                    data = self._average
                case 'Minimum':
                    self._average = np.minimum(self._average, data)
                    data = self._average
                case 'Average':
                    # Exponential averager with variable alpha for fast start-up.
                    self._count += 1
                    alpha = 1.0 / (self._count + 1)
                    if alpha < self._alpha:
                        alpha = self._alpha
                    self._average *= (1.0 - alpha)
                    self._average += data * alpha
                    data = self._average
                case _:
                    raise ValueError("Unknown mode")
        return data
