from . import Player, InvalidMoveError
import numpy as np

class Easy(Player):
    name = 'Easy'
    def _make_move(self, gui):
        if self.win_if_possible(gui): return
        if self.extend_three_to_four(gui): return
        if self.block_open_three(gui): return
        if self.block_doubly_open_two(gui): return
        if self.extend_two_to_three(gui): return
        try:
            gui.board[gui.board.height // 2, gui.board.width // 2] = self.color
        except InvalidMoveError:
            if self.extend_one(gui): return
            self.random_move(gui)
