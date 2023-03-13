##PyDosa TODO

### TODO List

#### Thing to Check

- Check that averaging gets reset properly when settings are changed. The one measurement cycle delay introduced by the threading may cause this to go wrong.

#### Known Issues

- You can bring up multiple instrument chooser dialogs.

- Simulator window sometimes loses simulator control panel if
  dragged to another screen.

- Spectrum can obscure the frequency labels. Need to clip Y.

- Simulator doesn't save amplitude units

#### Proposed Enhancements:

- Add driver for Rigol DS1000Z series oscilloscopes (currently under development).

- The GUI is pixel based. It may need scaling option for hi-resolution displays (e.g. 3840x2160). The plot size could be configurable parameters.

- Add option to enter explicit IP address. This may be useful if a firewall is blocking port 111 (TBC).

- Maybe Close Connection should close the simulator control panel?

- The 'delay' property can be reintroduced now that sim runs in thread

- The process 'after' loop keeps running when in the paused state or no instrument is open.

- Add Python type hints

- Preference to set #samples averaged

- Add more test cases

#### Simulator Enhancements

- Option to set # quantisation levels & Volts full-scale

#### Enhancements to Consider

- Should scope driver 'prepare' method cancel any math mode or decoding mode?

- Should widgets be in a panel on the right instead of top and bottom? They could be grouped into Vertical and Horizontal.
  Simulator controls could be in a separate window.

- Check-boxes to allow multiple plots for min, max, mean, etc?
