"Define the base class for players to be used in the game"

from .board import InvalidMoveError

class Player(object):
    """
    Describtion of a player to be used in the Game

    :param color:

        The color that the player plays as described in "board.py".

    """
    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        """
        Place a stone onto the `board`

        :param board:

            The game board as described in "board.py"

        """
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                try:
                    board[i,j] = self.color
                    return
                except InvalidMoveError:
                    pass

        raise RuntimeError('Could not find any valid move')

class Human(Player):
    """
    A human player using a gui for input.

    :param color:

        The color that the player plays as described in "board.py".

    :param board_gui:

        The gui to be used for the input. Should be of type
        ``BoardGui`` implemented in "gui.py".

    """
    def __init__(self, color, board_gui):
        self.color = color
        self.gui = board_gui

    def make_move(self, board):
        self.gui.renew_board()
        if hasattr(board, 'lastmove'):
            self.gui.highlight_lastmove()
        self.gui.color_in_turn = self.color
        self.gui.await_move()
