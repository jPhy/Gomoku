"""
Implement the game's gui

"""

try:
    # python 2
    import Tkinter as tk
    from tkMessageBox import Message
except ImportError:
    import tkinter as tk # python 3
    from tkinter.messagebox import Message

gui_invalid_move_message = Message(message='Invalid move!', icon='error', title='Gomoku')

import numpy as np
from .board import black,white,empty , InvalidMoveError

class BoardGui(object):
    """
    Gui of a Gomoku game board. Create a window with buttons
    associated to a game Board (see "board.py")

    :param board:

        The game board for which to create a gui.

    :param window:

        The window to attach the Gui to (new window by default)

    """
    def __init__(self, board, window):
        self.board = board
        self.window = window

        # create a grid of buttons

        def button_command(i,j):
            try:
                self.board[j,i] = self.color_in_turn
            except InvalidMoveError:
                gui_invalid_move_message.show()

        self.buttons = np.empty_like(board.board, dtype='object')
        for i in range(board.width):
            for j in range(board.height):
                current_button = self.buttons[j,i] = tk.Button(window,
                                                               command=lambda x=i, y=j: button_command(x,y)
                                                               )
                current_button.grid(row=i, column=j)

    def renew_board(self):
        "Draw the stone symbols onto the buttons"
        for i in range(self.board.width):
            for j in range(self.board.height):
                if self.board[j,i] == black:
                    self.buttons[j,i].config(text='b') # TODO: image, use "self.buttons[j,i].config(imag=...)"
                elif self.board[j,i] == white:
                    self.buttons[j,i].config(text='w') # TODO: image, use "self.buttons[j,i].config(imag=...)"
                elif self.board[j,i] == empty:
                    self.buttons[j,i].config(text='  ') # TODO: image, use "self.buttons[j,i].config(imag=...)"

    def await_move(self):
        "Wait for one move to be taken"
        moves_left = self.board.moves_left
        while self.board.moves_left == moves_left:
            self.window.update()
