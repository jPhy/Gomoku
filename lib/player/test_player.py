"Unit test for the player class"

import unittest
import numpy as np
try:
    import Tkinter as tk # python 2
except ImportError:
    import tkinter as tk # python 3
from ..board import Board, black, white
from ..gui import BoardGui
from . import *

class TestPlayer(unittest.TestCase):
    def test_base_error(self):
        board = Board(width=2, height=4)
        board_gui = BoardGui(board, tk.Tk())
        board_gui.in_game = True

        class DummyPlayer(Player):
            name = 'dummy player'
            _make_move = lambda self, *args, **kwargs: None

        white_player = DummyPlayer(white)
        self.assertRaisesRegexp(InvalidMoveError, 'Player "dummy player" did not place a stone.', white_player.make_move, board_gui)

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
