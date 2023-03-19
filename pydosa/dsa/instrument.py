"""
Instrument connections.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
import importlib
from tkinter import messagebox

import vxi11

from pydosa.dsa.scope_driver import ScopeDriver
from pydosa.util.chooser_dialog import ChooserDialog
from pydosa.util.preferences_manager import PreferencesManager
from pydosa.util.util import compatible_version


def choose_instrument(prefs: PreferencesManager, root) -> ScopeDriver | None:
    """Choose a VXI-11 instrument and locate a compatible driver."""
    plugins = prefs.config['DEVICE']['plugins'].split(',')

    # Prompt use to select a VXI-11 instrument
    devices = vxi11.list_devices()
    items = []
    devs = []
    for host in devices:
        instr = vxi11.Instrument(host)
        idn = instr.ask('*IDN?')
        fields = [host] + idn.strip().split(',')
        devs.append(fields)
        items.append('{} {} {}'.format(*fields))
        instr.close()

    if not devs:
        messagebox.showerror('Error', 'No VXI-11 devices found', parent=root)
        return None

    selected = ChooserDialog.ask(root, items, title='VXI-11 Instruments',
                                 message='Select instrument\n')
    if not selected:
        return None

    # Get details of selected instrument
    ip = selected.split()[0]
    fields = [d for d in devs if d[0] == ip]
    ip, make, model, serial, firmware = fields[0]

    # Find a compatible driver
    found = None
    try:
        for plugin in plugins:
            mod = importlib.import_module(plugin)
            driver_cls = getattr(mod, 'Driver')
            if make.startswith(driver_cls.make) and model in driver_cls.models:
                if compatible_version(driver_cls.min_firmware, firmware):
                    found = driver_cls
                    print('Loading plugin:', plugin)
                    break
                else:
                    msg = ('Upgrade {} to firmware {} or later'
                           .format(model, driver_cls.min_firmware))
                    raise Exception(msg)

        if found is None:
            raise Exception('No driver found for {}'.format(model))

    except Exception as exc:
        messagebox.showerror("Error", str(exc), parent=root)
        return None

    # Instantiate driver and connect it to instrument
    driver = found()  # Create instance
    instr = vxi11.Instrument(ip)
    driver.open(instr)

    return driver
