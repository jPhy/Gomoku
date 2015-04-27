"Define the base class for players to be used in the game"

from .board import InvalidMoveError
try:
    # python 2
    import Tkinter as tk
    from tkMessageBox import Message
except ImportError:
    # python 3
    import tkinter as tk
    from tkinter.messagebox import Message

class Player(object):
    """
    Describtion of a player to be used in the Game

    :param color:

        The color that the player plays as described in "board.py".

    """
    def __init__(self, color):
        self.color = color

    def make_move(self, gui):
        """
        Place a stone onto the `board`.
        This is a common function that *should not be overridden*.
        Override ``_make_move`` instead.

        :param gui:

            The game ``BoardGui`` as described in "gui.py"

        """
        gui.renew_board()
        if hasattr(gui.board, 'lastmove'):
            gui.highlight_lastmove()
        gui.color_in_turn = self.color
        moves_left = gui.board.moves_left

        self._make_move(gui)

        if not moves_left - 1 == gui.board.moves_left:
            raise RuntimeError('Could not find any valid move')

    def _make_move(self, gui):
        "Override this function for specific players"
        for i in range(gui.board.shape[0]):
            for j in range(gui.board.shape[1]):
                try:
                    gui.board[i,j] = self.color
                    return
                except InvalidMoveError:
                    pass

class Human(Player):
    """
    A human player using a gui for input.

    :param color:

        The color that the player plays as described in "board.py".

    """
    def _make_move(self, gui):
        # wait for user input
        moves_left = gui.board.moves_left
        while gui.board.moves_left == moves_left:
            try:
                gui.window.update()
            except tk.TclError:
                exit(0)
