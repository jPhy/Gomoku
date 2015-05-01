"Unit tests for the Random player"

import unittest
import numpy as np
from ..board import Board, black, white, empty
from ..gui import BoardGui, tk
from .random import *

class TestRandomPlayer(unittest.TestCase):
    def setUp(self):
        np.random.seed(42425243212)

        self.width = 20
        self.height = 10
        self.board = Board(self.height, self.width)
        self.board_gui = BoardGui(self.board, tk.Tk())
        self.board_gui.in_game = True

        self.white_player = Random(white)
        self.black_player = Random(black)

    def base_test(self):
        while self.board_gui.board.winner()[0] is None and not self.board_gui.board.full():
            self.white_player.make_move(self.board_gui)
            self.black_player.make_move(self.board_gui)
