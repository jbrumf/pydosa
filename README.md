## Pydosa - Digital Oscilloscope Spectrum Analyzer

Pydosa is a spectrum analyser application for use with VXI-11 compliant digital oscilloscopes. It currently has support for the Siglent SDS1000X-E and SDS1000X-U series oscilloscopes. The oscilloscope driver is written as a plugin to allow support to be added for other instruments.

Pydosa also has a built-in signal simulator. It was originally written to allow the software to be tested using signals with precisely known properties. However, it may be useful for demonstrating the program when a suitable oscilloscope is not available.

For installation instructions and other documentation see the [Pydosa Wiki](https://github.com/jbrumf/pydosa/wiki) :

- [User Guide](https://github.com/jbrumf/pydosa/wiki/User_Guide)

- [FFT Spectral Analysis](https://github.com/jbrumf/pydosa/wiki/Spectral_Analysis)

- [Writing an Oscilloscope Driver](https://github.com/jbrumf/pydosa/wiki/Writing_Driver)

- [README](https://github.com/jbrumf/pydosa#readme)

### System Requirements

* macOS, Windows 10 or Linux system
* Python 3.10 or later

It should also work on Windows 11, but this has not been tested.

### Instruments Supported

Pydosa currently supports the following oscilloscopes:

* Siglent SDS1104X-E, SDS1204X-E, SDS1104X-U

It has only been tested on the SDS1104X-E and SDS1204X-E, but is expected to work on the SDS1104X-U.

### License

MIT License (see LICENSE file)

### Known Issues

#### Networking Issues

Pydosa communicates with the oscilloscope using the VXI-11 protocol over the LAN. This sends a broadcast packet to port 111 to find any VXI-11 devices on the host's subnet. The devices respond by UDP from port 111. This provides plug-and-play operation without having to tell Pydosa the IP address of the oscilloscope and makes it possible for the oscilloscope to use a dynamically-allocated DHCP IP address.

This mechanism may fail if port 111 is blocked by a firewall.

* *Linux firewall:* The Linux firewall needs to configured to allow the incoming packets. For example, for an Ubuntu host on subnet 192.168.1.0/24:

`ufw allow from 192.168.1.0/24 proto udp port 111`

* *MacOS firewall:* If the macOS firewall is enabled, the Mac will prompt the user to accept the VXI-11 network connection. Once it has been accepted once, it should not prompt when run again.

#### Other Issues

- *Scope lock-up:* If Pydosa is killed while the oscilloscope is transferring data, it may cause the scope controls to lock up. To recover, power the scope off and on again.
