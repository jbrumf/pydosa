## PyDosa TODO

### TODO List

#### Known Issues

- You can bring up multiple instrument chooser dialogs.

- Simulator window sometimes loses simulator control panel if
  dragged to another screen.

- Spectrum can obscure the frequency labels. Need to clip Y.

- Power at Nyquist frequency should be halved as nsamples is even.

#### Proposed Enhancements:

- Add driver for Rigol DS1000Z series oscilloscopes (currently under development).

- The GUI is pixel based. It may need scaling option for hi-resolution displays (e.g. 3840x2160). The plot size could be
  configurable parameters.

- Add option to enter explicit IP address. This may be useful if a firewall is blocking port 111 (TBC).

- The 'delay' property could be reintroduced now that sim runs in thread

- The process 'after' loop keeps running when in the paused state or no instrument is open.

#### Simulator Enhancements

- Option to set # quantisation levels & Volts full-scale

#### Enhancements to Consider

- Should scope driver 'prepare' method cancel any math mode or decoding mode?
