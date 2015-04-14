"""
Implement the game board

This module defines the stone colors `empty`, `black` and `white`

"""

import numpy as np

# the colors
empty =  0
black = +1
white = -1

class InvalidMoveError(Exception):
    pass

class Board(object):
    """
    Gomoku game board of the desired size (`width`, `height`).
    Can access and place stones as ``self[x,y]``.
    Check if attempted moves are valid.

    """
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.shape = (self.width, self.height)
        self.board = np.zeros(self.shape, dtype='int8')

        self.moves_left = self.width * self.height
        self.in_turn = white

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        if value == self.in_turn and self[key] == empty:
            self.in_turn = - self.in_turn
            assert self.moves_left > 0
            self.moves_left -= 1
            self.board[key] = value

        else: # invalid move
            if   self[key] != empty:
                raise InvalidMoveError('Position %s is already taken' % ((key),))
            elif self.in_turn == black:
                raise InvalidMoveError('Black is in turn')
            elif self.in_turn == white:
                raise InvalidMoveError('White is in turn')
            else:
                raise RuntimeError('FATAL ERROR!')

    def full(self):
        "Return bool that indicates if the board has empty fields left"
        if self.moves_left:
            return False
        else:
            return True
