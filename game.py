#! /usr/bin/env python

try:
    # python 2
    import Tkinter as tk
    from tkMessageBox import Message
except ImportError:
    # python 3
    import tkinter as tk
    from tkinter.messagebox import Message
import lib

if __name__ == '__main__':
    main_window = lib.gui.MainWindow(16,13)
    main_window.mainloop()
