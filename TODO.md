## PyDosa TODO

### TODO List

#### Known Issues

- SDS1000X-U will not work with SDS1000X-E driver because the X-U firmware has independent version numbers. 

- The instrument chooser dialog should be modal. At the moment, it is possible to open more than one.

- The spectrum can obscure the frequency labels. The Y values should be clipped at the X axis.

- The power in the Nyquist frequency bin should be halved when the number of samples is even.


#### Proposed Enhancements:

- Add a driver for the Rigol DS1000Z series oscilloscopes (currently under development).

- The GUI is pixel based. It may need a scaling option for high-resolution displays (e.g. 3840x2160). The plot size
  could be a configurable parameter.

- Add an option to specify an explicit IP address as an alternative to VXI-11 device discovery. This would be helpful
  when a firewall is blocking port 111.

#### Simulator Enhancements

- It would be more natural to specify the number of quantization bits and vertical range than the delta-V per level.

#### Enhancements to Consider

- The scope driver 'prepare' method should perhaps cancel any math mode or decoding mode.

### Minor Remarks

- The process 'after' loop keeps running when in the paused state or no instrument is open.
