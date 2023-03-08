"""
Interactive test for frequency_widget.

This allows the widget to be exercised interactively.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
from tkinter import Frame
from tkinter import Tk

from pydosa.dsa.frequency_widget import FrequencyWidget


class FrequencyWidgetDemo(object):
    """Tests for frequency_widget."""

    def __init__(self, parent):
        self.main_frame = Frame(parent)
        self.main_frame.pack()
        self.freq_widget = FrequencyWidget(parent, self.func)
        self.freq_widget.pack()

    def func(self, x, y):
        print(x, y)


if __name__ == "__main__":
    root = Tk()
    root.geometry('%dx%d+%d+%d' % (500, 50, 10, 500))
    myapp = FrequencyWidgetDemo(root)
    root.mainloop()
