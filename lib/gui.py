"""
Implement the game's gui

"""

try:
    # python 2
    import Tkinter as tk
    from tkMessageBox import Message
except ImportError:
    # python 3
    import tkinter as tk
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

        The window to attach the gui to.

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
                    self.buttons[j,i].config(background='black', activebackground='black', highlightthickness=3, highlightbackground='lightgray')
                elif self.board[j,i] == white:
                    self.buttons[j,i].config(background='white', activebackground='white', highlightthickness=3, highlightbackground='lightgray')
                elif self.board[j,i] == empty:
                    self.buttons[j,i].config(background='darkgray', activebackground='darkgray', highlightthickness=3, highlightbackground='lightgray')

    def await_move(self):
        "Wait for one move to be taken"
        moves_left = self.board.moves_left
        while self.board.moves_left == moves_left:
            self.window.update()

    def highlight_winner(self, positions):
        """
        Highlight the buttons with the coordinates ``(y,x)``
        (see board.py) passed via ``positions``

        :param positions:
            iterable if tuples with the coordinates as specified in
            'board.py'

        """
        for y,x in positions:
            self.buttons[y,x].config(highlightbackground='red')

    def highlight_lastmove(self):
        """
        Highlight the button with the coordinates of the last move.

        """
        self.buttons[self.board.lastmove].config(highlightbackground='yellow')
