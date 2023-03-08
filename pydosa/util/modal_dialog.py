"""
Base class for Tkinter modal dialog.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2020 Jon Brumfitt
"""
from tkinter import Frame, Toplevel, Button


class ModalDialog(Toplevel):
    """Base class for Tkinter modal dialog."""

    def __init__(self, parent, title=None):
        """Initialization"""
        Toplevel.__init__(self, parent)
        self.parent = parent
        if title:
            self.title(title)
        self.transient(parent)  # Transient window drawn on top of parent
        self.grab_set()  # Receive all application event to make window modal
        self.protocol('WM_DELETE_WINDOW', self.cancel_callback)

        # Create the contents and buttons
        content_frame = Frame(self)
        self.create_content(content_frame)
        content_frame.pack(padx=5, pady=5)
        self.create_buttons()

        # Position the window relative to parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        self.wait_window(self)  # Wait until dialog closed

    def create_buttons(self):
        """Override to add custom button frame"""
        button_frame = Frame(self)
        button1 = Button(button_frame, text='OK', width=8, padx=10,
                         pady=5, command=self.ok_callback)
        button1.grid(row=0, column=0)
        button2 = Button(button_frame, text='Cancel', width=8, padx=10,
                         pady=5, command=self.cancel_callback)
        button2.grid(row=0, column=1)
        button1.focus_set()
        self.bind("<Return>", self.ok_callback)
        self.bind("<Escape>", self.cancel_callback)
        button_frame.pack(padx=5, pady=5)

    def create_content(self, content_frame):
        """Override to create content"""
        pass

    def validate(self):
        """Override to validate content"""
        return True

    def ok_action(self):
        """Override to handle OK action"""
        pass

    def ok_callback(self, event=None):
        """Handle callback from OK button"""
        if not self.validate():
            return

        self.withdraw()  # Hide window without destroying it yet
        self.update_idletasks()
        self.ok_action()
        self.parent.focus_set()
        self.destroy()  # Destroy the window

    def cancel_callback(self, event=None):
        """Handle callback from Cancel button"""
        self.parent.focus_set()
        self.destroy()  # Destroy the window
