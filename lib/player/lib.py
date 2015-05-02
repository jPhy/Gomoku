"Define basic subroutines useful for all AI players"

from ..board import black, white, empty
import numpy as np

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
    def win_if_possible(self, gui):
        """
        Place a stone where the player wins immediately if possible.
        Return ``True`` if a stone has been placed, otherwise return False.

        """
        line_getter_functions = [gui.board.get_column, gui.board.get_row,
                                 gui.board.get_diagonal_upleft_to_lowright,
                                 gui.board.get_diagonal_lowleft_to_upright]

        for i in range(gui.board.height):
            for j in range(gui.board.width):
                for f in line_getter_functions:
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
