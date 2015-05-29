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
    Gomoku game board of the desired size (`height`, `width`).
    Can access and place stones as ``self[y,x]``, where ``y``
    denotes the vertical and ``x`` the horizontal index.
    Check if attempted moves are valid.
    Coordinate system:

     ------------->  x
    |
    |
    |
    |
    V

    y

    """
    def __init__(self, height, width):
        self.height = int(height)
        self.width = int(width)
        self.shape = (self.height, self.width)
        self.board = np.zeros(self.shape, dtype='int8')

        self.reset()

    def reset(self):
        self.board[:] = empty
        self.moves_left = self.height * self.width
        self.in_turn = white
        if hasattr(self, 'lastmove'):
            del self.lastmove
        self.log = []

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        if value == self.in_turn and self[key] == empty:
            self.in_turn = - self.in_turn
            assert self.moves_left > 0
            self.moves_left -= 1
            self.board[key] = value
            self.lastmove = key
            self.log.append(key)

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

    get_line_functions_docstring = """
    Return an array from the position passed via `x` and `y` of length 5
    and a list of the coordinates of that line.

    .. note::

        The returned array is bound to the instance and NOT a copy.

    :param y, x:

        The indices of the left hand position to start the line.
        The direction is defined by the function name.

    """

    def get_column(self, y, x, length=5):
        __doc__ = self.get_line_functions_docstring
        line = np.empty(length, dtype='int8')
        for i in range(length):
            line[i] = self[y+i,x]
        return line, [(y+i,x) for i in range(length)]

    def get_row(self, y, x, length=5):
        __doc__ = self.get_line_functions_docstring
        line = np.empty(length, dtype='int8')
        for i in range(length):
            line[i] = self[y,x+i]
        return line, [(y,x+i) for i in range(length)]

    def get_diagonal_upleft_to_lowright(self, y, x, length=5):
        __doc__ = self.get_line_functions_docstring
        line = np.empty(length, dtype='int8')
        for i in range(length):
            line[i] = self[y+i,x+i]
        return line, [(y+i,x+i) for i in range(length)]

    def get_diagonal_lowleft_to_upright(self, y, x, length=5):
        __doc__ = self.get_line_functions_docstring
        line = np.empty(length, dtype='int8')
        if y < length - 1:
            raise IndexError
        for i in range(length):
            line[i] = self[y-i,x+i]
        return line, [(y-i,x+i) for i in range(length)]

    def winner(self):
        """
        Return the winner and the positions of the five in a line or None.

        .. note::

            If there are multiple lines of five, the first line that is found
            will be designated as winner. Therefore you should check for winner
            after EVERY move.

        """
        for i in range(self.height):
            for j in range(self.width):
                for getter_function in (self.get_row, self.get_column, self.get_diagonal_lowleft_to_upright, self.get_diagonal_upleft_to_lowright):
                    try:
                        line, positions = getter_function(i,j)
                    except IndexError:
                        continue
                    if abs(line.sum()) == 5:
                        return line[0], positions
        return None, []
