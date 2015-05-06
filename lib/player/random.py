from . import Player, InvalidMoveError
import numpy as np

class Random(Player):
    "An AI that randomly places stones."
    name = 'Random AI'
    def _make_move(self, gui):
        if self.win_if_possible(gui):
            return
        else:
            self.random_move(gui)
