### Pydosa - Digital Oscilloscope Spectrum Analyzer

Pydosa is a spectrum analyser application for use with Siglent SDS1000X-E series oscilloscopes.

The oscilloscope driver is written as a plugin to allow support to be added for other VXI-11 compliant instruments.

For documentation see the [Pydosa Wiki](https://github.com/jbrumf/pydosa/wiki).

#### Overview

Modern digital oscilloscopes typically have an FFT function that allows display of the signal spectrum. On low cost instruments it is often difficult to adjust the settings to obtain the desired spectrum plot.

Pydosa runs on a computer and connects to the oscilloscope via a LAN network. This allows a better user interface for easier control and display on a larger screen.

#### System Requirements

* macOS, Windows 10 or Linux system
* Python 3.10 or later

It should also work on Windows 11, but this has not been tested.

#### Instruments Supported

Pydosa currently supports the following oscilloscopes:

* Siglent SDS1104X-E, SDS1204X-E

#### Installation

To install from the source distribution using conda:

    cd pydosa
    conda env create -f environment.yml
    conda activate pydosa

To install from the source distribution using setuptools (with python>=3.10):

    cd pydosa
    python setup.py install

Pydosa may be made available as a PyPI and/or Conda package at a later date.

#### Running Pydosa

- Connect the oscilloscope to the LAN and configure its IP address
- Run: python -m pydosa
- Select instrument when prompted
- The spectrum window should appear after a few seconds
- Connect a signal to channel 1 of the oscilloscope
- Adjust the vertical gain on the oscilloscope

Pydosa controls the oscilloscope while it is running. The only controls you should adjust manually are those for the vertical channel to ensure that the waveform is filling several vertical divisions without clipping. If the input is clipped it will result in spurious spectral components. If the input level is too low it will increase the quantization noise.

If the instrument is not detected, check that the computer and oscilloscope are on the same LAN subnet. Problems may be encountered if there is a firewall blocking the connection (see Networking Issues below).

#### Simulator

Pydosa has a built-in signal simulator. It was originally written to allow Pydosa to be tested using signals with precisely known properties. However, it may be useful for demonstrating the program when a suitable oscilloscope is not available. To enter simulation mode, select `Open simulator` from the File menu. Controls for the simulator should appear on the right-hand side of the main window.

#### License

MIT License (see LICENSE file)

#### Networking Issues

Pydosa communicates with the oscilloscope using the VXI-11 protocol over the LAN. This sends a broadcast packet to port 111 to find any VXI-11 devices on the host's subnet. The devices respond by UDP from port 111. This provides plug-and-play operation without having to tell Pydosa the IP address of the oscilloscope and makes it possible for the oscilloscope to use a dynamically-allocated DHCP IP address.

This mechanism may fail if port 111 is blocked by a firewall.

* *Linux firewall:* The Linux firewall needs to configured to allow the incoming packets. For example, for an Ubuntu host on subnet 192.168.1.0/24:

`ufw allow from 192.168.1.0/24 proto udp port 111`

* *MacOS firewall:* If the macOS firewall is enabled, the Mac will prompt the user to accept the VXI-11 network connection. Once it has been accepted once, it should not prompt when run again.

#### Known Issues

- When entering numeric values, it is necessary to press Enter to accept the value. Simply changing the focus by selecting another widget is not sufficient.

- *Scope lock-up:* If Pydosa is killed while the oscilloscope scope is transferring data, it may cause the scope controls to lock up. To recover, power the scope off and on again.
