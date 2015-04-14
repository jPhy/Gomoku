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
