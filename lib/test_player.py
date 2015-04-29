"Unit test for the player class"

import unittest
import numpy as np
try:
    import Tkinter as tk # python 2
except ImportError:
    import tkinter as tk # python 3
from .board import Board, black, white
from .gui import BoardGui
from .player import *

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.width = 2 # must be even for this test_case
        self.height = 4 # must be even for this test_case
        self.board = Board(self.width, self.height)
        self.board_gui = BoardGui(self.board, tk.Tk())
        self.board_gui.in_game = True

        self.white_player = Player(white)
        self.black_player = Player(black)

    def test_base_error(self):
        self.white_player.make_move(self.board_gui)

        self.assertRaisesRegexp(RuntimeError, 'Could not find any valid move', self.white_player.make_move, self.board_gui)

    def test_moves(self):
        total_size = self.width * self.height // 2

        for i in range(total_size):
            self.white_player.make_move(self.board_gui)
            self.black_player.make_move(self.board_gui)

        np.testing.assert_equal(self.board.board.flatten(), np.array([white,black] * total_size))

class TestPlayerManagement(unittest.TestCase):
    def test_get_player_index(self):
        found_indices = []
        print(available_player_names)
        found_indices.append( get_player_index('Human') ) # no hint
        found_indices.append( get_player_index('Human', hint=0) ) # hint correct
        found_indices.append( get_player_index('Human', hint=1) ) # hint wrong

        for index in found_indices:
            self.assertEqual(index, 0)

        self.assertRaisesRegexp(ValueError, '"Foo".*not.*registered', get_player_index, 'Foo')
