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
from . import player, board
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

        self.buttons = np.empty_like(board.board, dtype='object')
        for i in range(self.board.width):
            for j in range(self.board.height):
                current_button = self.buttons[j,i] = tk.Button(window)
                current_button.grid(row=i, column=j)

    def game_running_buttons(self):
        def button_command(i,j):
            try:
                self.board[j,i] = self.board.in_turn
            except InvalidMoveError:
                gui_invalid_move_message.show()

        for i in range(self.board.width):
            for j in range(self.board.height):
                self.buttons[j,i].config( command=lambda x=i, y=j: button_command(x,y) )

    def game_running(self):
        self.in_game = True
        self.game_running_buttons()

    def game_over(self):
        self.in_game = False
        self.game_over_buttons()

    def game_over_buttons(self):
        def button_command():
            Message(message='The game is already over!\nStart a new game first.', icon='error', title='Gomoku').show()

        for i in range(self.board.width):
            for j in range(self.board.height):
                self.buttons[j,i].config(command=button_command)

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

class MainWindow(tk.Tk):
    """
    Gui of Gomoku; the main window.

    :param width, height:

        width and height of the Gomoku game board

    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        tk.Tk.__init__(self)
        self.title('Gomoku')

        self.canvas_board = tk.Canvas(self)
        self.canvas_board.pack()

        self.canvas_controls = tk.Canvas(self)
        self.canvas_controls.pack(side='bottom')
        self.new_game_button = tk.Button(self.canvas_controls, text='New game', command=self.new_game)
        self.new_game_button.grid(column=0, row=0)
        self.options_button = tk.Button(self.canvas_controls, text='Options', command=self.options)
        self.options_button.grid(column=1, row=0)
        self.exit_button = tk.Button(self.canvas_controls, text='Exit', command=self.exit)
        self.exit_button.grid(column=2, row=0)

        self.board = board.Board(self.width,self.height)
        self.gui = BoardGui(self.board, self.canvas_board)

    def exit(self):
        self.destroy()

    def mainloop(self):
        self.new_game()
        while True:
            self.update()

    def new_game(self):
        self.gui.game_running()

        self.board.reset()
        self.gui.renew_board()
        # white_player = player.Human(board.white)
        white_player = player.Player(board.white)
        black_player = player.Human(board.black)
        # black_player = player.Player(board.black)

        moves_left = self.board.moves_left

        while True:
            white_player.make_move(self.gui)
            self.gui.window.update()

            winner, positions = self.board.winner()
            if (winner is not None) or (self.board.full()):
                break

            black_player.make_move(self.gui)
            self.gui.window.update()

            winner, positions = self.board.winner()
            if (winner is not None) or (self.board.full()):
                break

        self.gui.renew_board()
        self.gui.highlight_winner(positions)
        if not self.gui.in_game:
            return
        elif winner == white:
            Message(message='White wins!', icon='info', title='Gomoku').show()
        elif winner == black:
            Message(message='Black wins!', icon='info', title='Gomoku').show()
        elif winner is None:
            Message(message='Draw!', icon='info', title='Gomoku').show()
        else:
            raise RuntimeError('FATAL ERROR')

        self.gui.game_over()

    def options(self):
        raise NotImplementedError
