"""
Abstract base class for an oscilloscope driver.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""

from abc import ABC, abstractmethod

from numpy import array as npa


class ScopeDriver(ABC):
    """Abstract base class for an oscilloscope driver."""

    @property
    @abstractmethod
    def make(self) -> str:
        """Abstract property for the make of instrument."""
        pass

    @property
    @abstractmethod
    def models(self) -> list[str]:
        """Abstract property for list of model numbers."""
        pass

    @property
    @abstractmethod
    def min_firmware(self) -> str:
        """Abstract property for the minimum firmware version."""
        pass

    @property
    @abstractmethod
    def sample_rates(self) -> list[str]:
        """Abstract property for the list of sample rates."""
        pass

    @property
    @abstractmethod
    def sample_sizes(self) -> list[str]:
        """Abstract property for the list of sample sizes."""
        pass

    @property
    def initial_sample_size(self) -> str:
        """Property for default sample size.
           The default is the first value in the list.
        """
        return self.sample_sizes[0]

    @property
    def initial_sample_rate(self) -> str:
        """Property for default sample rate.
           The default is the first value in the list.
        """
        return self.sample_rates[0]

    @abstractmethod
    def open(self, instrument) -> None:
        """Open the driver.
        The instrument object is the VXI-11 Instrument.
        :param instrument: Connection to a VXI-11 instrument
        """
        pass

    @abstractmethod
    def prepare(self) -> None:
        """Configure the instrument.

        This method is called once to initialize the instrument to
        a known initial state. For example, it could ensure that
        only channel 1 is active.
        """
        pass

    @abstractmethod
    def fetch_data(self, nsamples: int, srate_option: str) -> tuple[npa, float]:
        """Acquire sample data, scaled to volts
        :param nsamples: Number of samples
        :param srate_option: Sample rate
        :return: (samples, srate)
        """
        pass

    @abstractmethod
    def close(self):
        """Close the driver"""
        pass
