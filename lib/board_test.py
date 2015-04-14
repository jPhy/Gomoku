"Unit test for the game-board class"

import unittest
from .board import *

def place_stone(board, color, x, y):
    board[x,y] = color

class TestBoard(unittest.TestCase):
    def test_creation(self):
        width = 20
        height = 40
        board = Board(width, height)

        self.assertEqual(board.shape, (height,width))
        for i in range(width):
            for j in range(height):
                # empty refers to "no stone laid" and should be defined in the module ``board``
                self.assertEqual(board[j,i], empty)

    def test_lay_stone(self):
        width = height= 20
        board = Board(width, height)

        # try "place a black stone at 5,5" --> white starts therefore expect error
        self.assertRaisesRegexp(InvalidMoveError, 'White is in turn', place_stone, board, black, 5, 5)

        # "place a white stone at 5,5" should be OK
        place_stone(board, white, 5, 5)

        # "place another white stone" is an invalid move
        self.assertRaisesRegexp(InvalidMoveError, 'Black is in turn', place_stone, board, white, 5, 4)

        # place black stone at 5,5 is invalid since 5,5 is already occupied
        self.assertRaisesRegexp(InvalidMoveError, r'Position \(5, 5\) is already taken', place_stone, board, white, 5, 5)

    def test_full(self):
        width = height= 4
        board = Board(width, height)
        in_turn = white

        for i in range(width):
            for j in range(height):
                board[i,j] = in_turn
                if in_turn == white:
                    in_turn = black
                else:
                    in_turn = white
                if not (i,j) == (width-1, height-1):
                    self.assertFalse(board.full())
                else:
                    self.assertTrue(board.full())

        self.assertTrue(board.full())

    def test_winner(self):
        width = height= 10
        board = Board(width, height)

        self.assertTrue(board.winner() is None)
        place_stone(board, white, 1,2)
        self.assertTrue(board.winner() is None)
        place_stone(board, black, 0,2)
        self.assertTrue(board.winner() is None)
        place_stone(board, white, 1,3)
        self.assertTrue(board.winner() is None)
        place_stone(board, black, 0,3)
        self.assertTrue(board.winner() is None)
        place_stone(board, white, 1,4)
        self.assertTrue(board.winner() is None)
        place_stone(board, black, 0,4)
        self.assertTrue(board.winner() is None)
        place_stone(board, white, 1,5)
        self.assertTrue(board.winner() is None)
        place_stone(board, black, 0,5)
        self.assertTrue(board.winner() is None)
        place_stone(board, white, 1,6)
        self.assertTrue(board.winner() == white)

class TestGetLine(unittest.TestCase):
    def setUp(self):
        self.target_shape = (5,)

        width = 7
        height = 7
        self.board = Board(width=width, height=height)

        # make column
        place_stone(self.board, white, 1,2)
        place_stone(self.board, black, 1,3)
        place_stone(self.board, white, 1,4)
        place_stone(self.board, black, 1,5)
        place_stone(self.board, white, 1,6)

        # make row
        place_stone(self.board, black, 2,6)
        place_stone(self.board, white, 3,6)
        place_stone(self.board, black, 4,6)
        place_stone(self.board, white, 5,6)
        # leave (6,6) empty

        # make diagonal lowleft to upright
        place_stone(self.board, black, 0,0)
        place_stone(self.board, white, 1,1)
        place_stone(self.board, black, 2,2)
        place_stone(self.board, white, 3,3)
        place_stone(self.board, black, 4,4)

        # make diagonal upleft to lowright
        # (1,4) is already white from "make column"
        place_stone(self.board, white, 2,3)
        place_stone(self.board, black, 3,2)
        # leave (4,1) empty
        place_stone(self.board, white, 5,0)

    def test_get_row(self):
        row = self.board.get_row(2,6)
        self.assertEqual(row.shape, self.target_shape)
        np.testing.assert_equal(row, np.array([black,white,black,white,empty]))

    def test_get_column(self):
        column = self.board.get_column(1,2)
        self.assertEqual(column.shape, self.target_shape)
        np.testing.assert_equal(column, np.array([white,black,white,black,white]))

    def test_get_diagonal_lowleft_to_upright(self):
        diagonal = self.board.get_diagonal_lowleft_to_upright(0,0)
        self.assertEqual(diagonal.shape, self.target_shape)
        np.testing.assert_equal(diagonal, np.array([black,white,black,white,black]))

    def test_diagonal_upleft_to_lowright(self):
        diagonal = self.board.get_diagonal_upleft_to_lowright(1,4)
        self.assertEqual(diagonal.shape, self.target_shape)
        np.testing.assert_equal(diagonal, np.array([white,white,black,empty,white]))
