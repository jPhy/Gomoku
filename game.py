#! /usr/bin/env python

from __future__ import print_function
import lib

class ErrorHandler(object):
    def __enter__(self):
        pass

    def __exit__(self, error_type, error_args, traceback):
        if error_type is lib.gui.tk.TclError:
            print("WARNING: A GUI-related `TclError` error occurred:", error_args)
            return True # do not reraise error
        return False # reraise nonTcl errors

if __name__ == '__main__':
    main_window = lib.gui.MainWindow(16,13)
    with ErrorHandler():
        main_window.mainloop()
