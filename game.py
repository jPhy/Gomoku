#! /usr/bin/env python

from __future__ import print_function
import lib

class ErrorHandler(object):
    def __enter__(self):
        pass

    def __exit__(self, error_type, error_args, traceback):
        if error_type is None:
            return
        if error_type is lib.gui.tk.TclError:
            print("WARNING: A GUI-related `TclError` error occurred:", error_args)
            return True # do not reraise error
        # else:
        # GUIify errors
        if issubclass(error_type, Exception): # Only catch real exceptions not ``BaseException``
            lib.gui.Message(message=repr(error_args), icon='warning', title='Gomoku - error').show()
        return False # reraise nonTcl errors => stderr message and nonzero exit

if __name__ == '__main__':
    main_window = lib.gui.MainWindow(13,16)
    with ErrorHandler():
        main_window.mainloop()
