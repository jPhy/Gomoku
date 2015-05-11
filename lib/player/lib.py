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
    def line_getter_functions(self, gui, length=5):
        return [lambda x,y: gui.board.get_column(x,y,length=length), lambda x,y: gui.board.get_row(x,y, length=length),
                lambda x,y: gui.board.get_diagonal_upleft_to_lowright(x,y, length=length),
                lambda x,y: gui.board.get_diagonal_lowleft_to_upright(x,y, length=length)]


    def random_move(self, gui):
        moves_left = gui.board.moves_left
        while moves_left == gui.board.moves_left:
            x = np.random.randint(gui.board.width)
            y = np.random.randint(gui.board.height)
            try:
                gui.board[y,x] = self.color
            except InvalidMoveError:
                continue

    def extend_one(self, gui):
        "Place a stone next to another one but only if extendable to five."
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                # search pattern: one of own color and four empty
                    if len(np.where(line == empty)[0]) == 4 and len(np.where(line == self.color)[0]) == 1:
                        index_own_color = np.where(line == self.color)[0][0]
                        if index_own_color == 0:
                            gui.board[positions[1]] = self.color
                            return True
                        else:
                            gui.board[positions[index_own_color - 1]] = self.color
                            return True
        return False

    def block_open_four(self, gui):
        "Block a line of four stones if at least one end open."
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue

                    # selection: search four of opponent's color and one empty
                    if len(np.where(line == empty)[0]) == 1 and len(np.where(line == -self.color)[0]) == 4:
                        index_of_empty = np.where(line == empty)[0][0]
                        gui.board[positions[index_of_empty]] = self.color
                        return True
        return False

    def block_doubly_open_two(self, gui):
        "Block a line of two if both sides are open."
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue

                    # select pattern [<all empty>, <opponent's color>, <opponent's color>, <all empty>]
                    if ( line == (empty, -self.color, -self.color, empty, empty) ).all():
                        gui.board[positions[3]] = self.color
                        return True

                    elif ( line == (empty, empty, -self.color, -self.color, empty) ).all():
                        gui.board[positions[1]] = self.color
                        return True

        return False

    def block_twice_to_three_or_more(self, gui):
        'Prevent opponent from closing two lines of three or more simultaneously.'
        line_getter_functions = self.line_getter_functions(gui)
        line_positions = []
        getter_functions = []
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in line_getter_functions:
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                    # search two of opponent's color and three empty in two crossing lines at an empty position
                    opponent_stones_in_line = len(np.where(line == -self.color)[0])
                    if opponent_stones_in_line >= 2 and len(np.where(line == empty)[0]) == 5 - opponent_stones_in_line:
                        for oldpos, old_getter in zip(line_positions, getter_functions):
                            for pos in positions:
                                if f != old_getter and pos in oldpos and gui.board[pos] == empty:
                                    gui.board[pos] = self.color
                                    return True
                        line_positions.append(positions)
                        getter_functions.append(f)
        return False

    def block_open_three(self, gui):
        "Block a line of three."
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue

                    # selection: search three of opponent's color and two empty
                    if len(np.where(line == empty)[0]) == 2 and len(np.where(line == -self.color)[0]) == 3:
                        indices_empty = np.where(line == empty)[0]
                        if 0 not in indices_empty:
                            gui.board[positions[indices_empty[0]]] = self.color
                            return True
                        else:
                            gui.board[positions[indices_empty[1]]] = self.color
                            return True
        return False

    def block_open_two(self, gui):
        "Block a line of two."
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                    # selection: search pattern [<all empty or bpundary>, opponent, opponent, <all empty or boundary>]
                    if len(np.where(line == empty)[0]) == 3 and len(np.where(line == -self.color)[0]) == 2:
                        indices_opponent = np.where(line == -self.color)[0]
                        if indices_opponent[1] == indices_opponent[0] + 1:
                            if indices_opponent[0] == 0:
                                gui.board[positions[3]] = self.color
                                return True
                            else:
                                gui.board[positions[indices_opponent[0]-1]] = self.color
                                return True
        return False

    def block_doubly_open_three(self, gui):
        "Block a line of three but only if both sides are open."
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue

                    if ( line == (empty, -self.color, -self.color, -self.color, empty) ).all():
                        gui.board[positions[0]] = self.color
                        return True
        return False

    def extend_three_to_four(self, gui):
        """
        Extend a line of three stones to a line of four stones but only
        if there is enough space to be completed to five.

        """
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                    # selection: search three of own color and two empty
                    if len(np.where(line == empty)[0]) == 2 and len(np.where(line == self.color)[0]) == 3:
                        indices_empty = np.where(line == empty)[0]
                        if 0 not in indices_empty:
                            gui.board[positions[indices_empty[0]]] = self.color
                            return True
                        else:
                            gui.board[positions[indices_empty[1]]] = self.color
                            return True
        return False

    def extend_three_to_doubly_open_four(self, gui):
        """
        Extend a line of three stones to a line of four stones but only
        if there is enough space to be completed to five ON BOTH SIDES.

        """
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui, length=6):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                    # selection: search pattern [empty, <extendable to 4 times own>, empty]
                    if len(np.where(line == empty)[0]) == 3 and len(np.where(line == self.color)[0]) == 3:
                        indices_empty = np.where(line == empty)[0]
                        if not (line[0] == empty and line[-1] == empty):
                            continue
                        else:
                            gui.board[positions[indices_empty[1]]] = self.color
                            return True
        return False

    def extend_two_to_three(self, gui):
        """
        Extend a line of two stones to a line of three stones but only
        if there is enough space to be completed to five.

        """
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in self.line_getter_functions(gui):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                    # selection: search two of own color and three empty
                    if len(np.where(line == empty)[0]) == 3 and len(np.where(line == self.color)[0]) == 2:
                        indices_empty = np.where(line == empty)[0]
                        gui.board[positions[indices_empty[np.random.randint(3)]]] = self.color
                        return True
        return False

    def extend_twice_two_to_three(self, gui):
        """
        Extend two crossing lines of two stones to two lines of three
        stones but only if there is enough space to be completed to five.

        """
        line_positions = []
        getter_functions = []
        for f in self.line_getter_functions(gui):
            for i in range(gui.board.height):
                for j in range(gui.board.width):
                    try:
                        line, positions = f(i,j)
                    except IndexError:
                        continue
                    # search two of own color and three empty in two crossing lines at an empty position
                    if len(np.where(line == empty)[0]) == 3 and len(np.where(line == self.color)[0]) == 2:
                        for oldpos, old_getter in zip(line_positions, getter_functions):
                            for pos in positions:
                                if f != old_getter and pos in oldpos and gui.board[pos] == empty:
                                    gui.board[pos] = self.color
                                    return True
                        line_positions.append(positions)
                        getter_functions.append(f)
        return False

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
