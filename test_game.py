"Unit test for the main game"

import unittest
import numpy as np
from game import *

class TestGame(unittest.TestCase):
    def test_play(self):
        width = 4
        height = 10
        black = lib.board.black
        white = lib.board.white
        empty = lib.board.empty

        board = lib.board.Board(height, width)
        white_player = lib.player.Player(white)
        black_player = lib.player.Player(black)

        winner, positions = play_game(white_player, black_player, board)

        target_final_board = np.array([
            [white, black, white, black],
            [white, black, white, black],
            [white, black, white, black],
            [white, black, white, black],
            [white, empty, empty, empty],
            [empty, empty, empty, empty],
            [empty, empty, empty, empty],
            [empty, empty, empty, empty],
            [empty, empty, empty, empty],
            [empty, empty, empty, empty],
        ])

        np.testing.assert_equal(board.board, target_final_board)

        self.assertEqual(winner, white)
        self.assertEqual(positions, [(0,0), (1,0), (2,0), (3,0), (4,0)])
