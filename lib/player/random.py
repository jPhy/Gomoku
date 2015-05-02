from . import Player, InvalidMoveError
import numpy as np

class Random(Player):
    "An AI that randomly places stones."
    name = 'Random AI'
    def _make_move(self, gui):
        if self.win_if_possible(gui):
            return
        moves_left = gui.board.moves_left
        if moves_left > 0:
            while moves_left == gui.board.moves_left:
                x = np.random.randint(gui.board.width)
                y = np.random.randint(gui.board.height)
                try:
                    gui.board[y,x] = self.color
                except InvalidMoveError:
                    continue
