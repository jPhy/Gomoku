"Unit tests for the Random player"

import unittest
import numpy as np
from ..board import Board, black, white, empty
from ..gui import BoardGui, tk
from .lib import Playerlibrary, PlayerTest
build_board = PlayerTest.build_board

class TestBuildBoard(unittest.TestCase):
    def test_ensure_no_winner(self):
        board_array = [[empty, black, empty, black, empty],
                       [white, white, white, white, white],
                       [black, empty, black, empty, black]]

        self.assertRaises(AssertionError, build_board, board_array)

    def test_build_equal_black_white(self):
        board_array = [[empty, black, empty, empty, empty, empty, empty, empty, empty, empty],
                       [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty],
                       [white, empty, empty, empty, empty, empty, white, empty, empty, empty],
                       [white, empty, empty, empty, empty, white, empty, empty, empty, empty],
                       [black, empty, empty, empty, empty, empty, empty, empty, empty, empty],
                       [empty, empty, empty, empty, empty, black, black, empty, empty, empty]]

        board = build_board(board_array)

        np.testing.assert_equal(board.board, np.array(board_array))
        self.assertEqual(board.moves_left, 10 * 6 - 8)

    def test_build_one_more_white_than_black(self):
        board_array = [[empty, black, empty, empty, empty, empty, empty, empty, empty, empty],
                       [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty],
                       [white, empty, empty, empty, empty, empty, white, empty, empty, empty],
                       [white, empty, empty, empty, empty, white, empty, white, empty, empty],
                       [black, empty, empty, empty, empty, empty, empty, empty, empty, empty],
                       [empty, empty, empty, empty, empty, black, black, empty, empty, empty]]

        board = build_board(board_array)

        np.testing.assert_equal(board.board, np.array(board_array))
        self.assertEqual(board.moves_left, 10 * 6 - 9)

class TestPlayerlibrary(unittest.TestCase):
    def setUp(self):
        np.random.seed(894763834)

        self.white_player = Playerlibrary()
        self.white_player.color = white

        self.black_player = Playerlibrary()
        self.black_player.color = black

    def test_win_if_possible(self):
        boards_to_test = \
        [
            # row - white
            [[white, white, empty, white, white, empty, empty, empty, empty, empty],
             [black, empty, black, black, black, empty, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty]],

            # column - black
            [[white, black, white, empty, empty, empty, empty, empty, empty, empty],
             [empty, black, empty, empty, empty, empty, empty, empty, empty, empty],
             [white, empty, empty, empty, empty, empty, empty, empty, empty, empty],
             [white, black, empty, empty, empty, empty, empty, empty, empty, empty],
             [white, black, empty, empty, empty, empty, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty]],

            # diagonal - black
            [[white, white, empty, empty, empty, white, empty, empty, empty, empty],
             [empty, black, empty, empty, empty, empty, empty, empty, empty, empty],
             [empty, empty, black, white, empty, empty, empty, empty, empty, empty],
             [empty, white, empty, black, empty, empty, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, black, empty, empty, empty, empty]],

            # diagonal - whtie
            [[empty, empty, empty, empty, empty, black, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, white, empty, empty],
             [empty, black, empty, empty, empty, empty, white, empty, empty, empty],
             [empty, empty, empty, empty, empty, white, empty, empty, black, empty],
             [empty, empty, empty, empty, white, empty, black, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty]],

            # not immediately winnable - whtie
            [[empty, empty, empty, empty, empty, black, empty, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, white, empty, empty],
             [empty, black, empty, empty, empty, empty, empty, empty, empty, empty],
             [empty, empty, white, empty, empty, white, empty, empty, black, empty],
             [empty, empty, empty, empty, white, empty, black, empty, empty, empty],
             [empty, empty, empty, empty, empty, empty, empty, empty, empty, empty]]
        ]

        for board_array in boards_to_test[:-1]:
            board = build_board(board_array)
            gui = BoardGui(board, tk.Tk())
            gui.in_game = True
            if board.in_turn == white:
                return_value = self.white_player.win_if_possible(gui)
                self.assertEqual(board.winner()[0], white)
            elif board.in_turn == black:
                return_value = self.black_player.win_if_possible(gui)
                self.assertEqual(board.winner()[0], black)
            else:
                raise RuntimeError('FATAL ERROR')
            self.assertTrue(return_value)

        board = build_board(boards_to_test[-1])
        return_value = self.black_player.win_if_possible(gui)
        self.assertFalse(return_value)
        self.assertEqual(board.moves_left, 52)
