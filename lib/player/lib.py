"Define basic subroutines useful for all AI players"

from ..board import black, white, empty, Board, InvalidMoveError
import numpy as np
import unittest

class Playerlibrary(object):
    """
    A library class that holds basic subroutines that are useful for all
    kinds of artificial-intelligence-type (AI-type) players, e.g. the
    function ``win_if_possible`` that checks if the game can be won in
    the next move.
    All the functions are written to take the same arguments as
    ``Player.make_move`` such that the call from within ``make_move``
    looks like e.g. ``self.win_if_possible(gui)``.

    """
    line_getter_functions = lambda self, gui: [gui.board.get_column, gui.board.get_row,
                                               gui.board.get_diagonal_upleft_to_lowright,
                                               gui.board.get_diagonal_lowleft_to_upright]


    def random_move(self, gui):
        moves_left = gui.board.moves_left
        while moves_left == gui.board.moves_left:
            x = np.random.randint(gui.board.width)
            y = np.random.randint(gui.board.height)
            try:
                gui.board[y,x] = self.color
            except InvalidMoveError:
                continue

    def win_if_possible(self, gui):
        """
        Place a stone where the player wins immediately if possible.
        Return ``True`` if a stone has been placed, otherwise return False.

        """
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                    # selection:
                    #            - can only place stones where field is ``empty``
                    #            - line must sum to "+" or "-" 4 (4 times black=+1 or white=-1 and once empty=0)

                    # place stone if that leads to winning the game
                    if empty in line and line.sum() == self.color * 4:
                        for pos in positions:
                            if gui.board[pos] == empty:
                                gui.board[pos] = self.color
                                return True
                        raise RuntimeError("Check the implementation of ``win_if_possible``.")
        # control reaches this point only if no winning move is found
        return False

class PlayerTest(unittest.TestCase):
    """
    Library class for testing AI players.

    Usage:
    Create a subclass and set the member variable ``Player`` to the
    AI you want to test:

    >>> class MyTest(PlayerTest):
    ...     Player = <Your AI>

    """

    Player = None

    @classmethod
    def build_board(self, board_array):
        """
        Build up a valid ``GameBoard`` holding the desired ``board_array``.

        .. note::

            You probably rather need `.build_gui`

        :param board_array:

            2D-array; e.g. [[white, empty],
                            [black, black]]

        """
        board_array = np.asarray(board_array, dtype=int)
        assert len(board_array.shape) == 2
        height = board_array.shape[0]
        width = board_array.shape[1]

        board = Board(width=width, height=height)

        white_indices = []
        black_indices = []

        # find positions that are not empty
        for i in range(height):
            for j in range(width):
                value = board_array[i,j]
                if value == empty:
                    continue
                elif value == white:
                    white_indices.append((i,j))
                elif value == black:
                    black_indices.append((i,j))
                else:
                    raise AssertionError("Invalid ``board_array``")

        # in a valid board, there are equally many black and white stones or
        # one more white that black stone since white begins
        assert len(white_indices) == len(black_indices) or len(white_indices) == len(black_indices) + 1

        while black_indices:
            board[white_indices.pop()] = white
            board[black_indices.pop()] = black

        assert board.winner()[0] is None

        # if there is one more white stone
        if white_indices:
            board[white_indices.pop()] = white

        return board

    @classmethod
    def build_gui(self, board_array):
        """
        Build up a valid ``GameBoard`` packed in a ``BoardGui`` holding
        the desired ``board_array``. The returned instance of ``BoardGui``
        is ready to use in ``Player.make_move()``.

        :param board_array:

            2D-array; e.g. [[white, empty],
                            [black, black]]

        """
        from ..gui import BoardGui, tk
        board = self.build_board(board_array)
        gui = BoardGui(board, tk.Tk())
        gui.in_game = True
        return gui

    def base_test(self):
        width = 20
        height = 10
        board = Board(height, width)
        from ..gui import BoardGui, tk
        board_gui = BoardGui(board, tk.Tk())
        board_gui.in_game = True

        if self.Player is not None:
            white_player = self.Player(white)
            black_player = self.Player(black)

            while board_gui.board.winner()[0] is None and not board_gui.board.full():
                white_player.make_move(board_gui)
                black_player.make_move(board_gui)
