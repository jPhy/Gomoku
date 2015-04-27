"Unit test for the game-board class"

import unittest
from .board import *

def place_stone(board, color, x, y):
    board[x,y] = color

class TestBoard(unittest.TestCase):
    def test_creation(self):
        width = 20
        height = 40
        board = Board(height, width)

        self.assertEqual(board.shape, (height,width))
        for i in range(height):
            for j in range(width):
                # empty refers to "no stone laid" and should be defined in the module ``board``
                self.assertEqual(board[i,j], empty)

    def test_reset(self):
        width = 20
        height = 40
        board = Board(height, width)
        place_stone(board, white, 5, 5)
        place_stone(board, black, 4, 5)
        place_stone(board, white, 4, 3)

        self.assertEqual(board.in_turn, black)
        self.assertFalse( (board.board == np.zeros([height, width]) ).all() )

        board.reset()

        self.assertEqual(board.in_turn, white)

        self.assertEqual(board.shape, (height,width))
        for i in range(height):
            for j in range(width):
                # empty refers to "no stone laid" and should be defined in the module ``board``
                self.assertEqual(board[i,j], empty)

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
        board = Board(height, width)
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

        self.assertEqual(board.winner(), (None, []))
        place_stone(board, white, 1,2)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, black, 0,2)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, white, 1,3)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, black, 0,3)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, white, 1,4)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, black, 0,4)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, white, 1,5)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, black, 0,5)
        self.assertEqual(board.winner(), (None, []))
        place_stone(board, white, 1,6)
        self.assertEqual(board.winner()[0], white)
        self.assertEqual(board.winner()[1], [(1,2), (1,3), (1,4), (1,5), (1,6)])

class TestGetLine(unittest.TestCase):
    def setUp(self):
        self.target_shape = (5,)

        width = 7
        height = 7
        self.board = Board(width=width, height=height)

        # make row
        place_stone(self.board, white, 1,2)
        place_stone(self.board, black, 1,3)
        place_stone(self.board, white, 1,4)
        place_stone(self.board, black, 1,5)
        place_stone(self.board, white, 1,6)

        # make column
        place_stone(self.board, black, 2,6)
        place_stone(self.board, white, 3,6)
        place_stone(self.board, black, 4,6)
        place_stone(self.board, white, 5,6)
        # leave (6,6) empty

        # make diagonal upleft to lowright
        place_stone(self.board, black, 0,0)
        place_stone(self.board, white, 1,1)
        place_stone(self.board, black, 2,2)
        place_stone(self.board, white, 3,3)
        place_stone(self.board, black, 4,4)

        # make diagonal lowleft to upright
        place_stone(self.board, white, 5,0)
        # leave (4,1) empty
        place_stone(self.board, black, 3,2)
        place_stone(self.board, white, 2,3)
        # (1,4) is already white from "make column"

    def test_get_column(self):
        column, positions = self.board.get_column(2,6)
        target_positions = [(2,6), (3,6), (4,6), (5,6), (6,6)]
        self.assertEqual(column.shape, self.target_shape)
        np.testing.assert_equal(column, np.array([black,white,black,white,empty]))
        self.assertEqual(positions, target_positions)

    def test_get_row(self):
        row, positions = self.board.get_row(1,2)
        target_positions = [(1,2), (1,3), (1,4), (1,5), (1,6)]
        self.assertEqual(row.shape, self.target_shape)
        np.testing.assert_equal(row, np.array([white,black,white,black,white]))
        self.assertEqual(positions, target_positions)

    def test_get_diagonal_upleft_to_lowright(self):
        diagonal, positions = self.board.get_diagonal_upleft_to_lowright(0,0)
        target_positions = [(0,0), (1,1), (2,2), (3,3), (4,4)]
        self.assertEqual(diagonal.shape, self.target_shape)
        np.testing.assert_equal(diagonal, np.array([black,white,black,white,black]))
        self.assertEqual(positions, target_positions)

    def test_diagonal_lowleft_to_upright(self):
        diagonal, positions = self.board.get_diagonal_lowleft_to_upright(5,0)
        target_positions = [(5,0), (4,1), (3,2), (2,3), (1,4)]
        self.assertEqual(diagonal.shape, self.target_shape)
        np.testing.assert_equal(diagonal, np.array([white,empty,black,white,white]))
        self.assertEqual(positions, target_positions)
