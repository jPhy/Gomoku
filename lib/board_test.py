"Unit test for the game-board class"

import unittest
from .board import *

class TestBoard(unittest.TestCase):
    def test_creation(self):
        width = 20
        height = 40
        board = Board(width, height)

        self.assertEqual(board.shape, (width,height))
        for i in range(width):
            for j in range(height):
                # empty refers to "no stone laid" and should be defined in the module ``board``
                self.assertEqual(board[i,j], empty)

    def test_lay_stone(self):
        width = height= 20
        board = Board(width, height)

        def place_stone(color, x, y):
            board[x,y] = color

        # try "place a black stone at 5,5" --> white starts therefore expect error
        self.assertRaisesRegexp(InvalidMoveError, 'White is in turn', place_stone, black, 5, 5)

        # "place a white stone at 5,5" should be OK
        place_stone(white, 5, 5)

        # "place another white stone" is an invalid move
        self.assertRaisesRegexp(InvalidMoveError, 'Black is in turn', place_stone, white, 5, 4)

        # place black stone at 5,5 is invalid since 5,5 is already occupied
        self.assertRaisesRegexp(InvalidMoveError, r'Position \(5, 5\) is already taken', place_stone, white, 5, 5)

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
