#! /usr/bin/env python

import lib

def play_game(white_player, black_player, game_board):
    """
    Play a game of gomoku.

    :param white_player, black_player:

        The players that shall play the game as defined in ``lib.players``

    :param game_board:

        Instance of ``lib.board.Board``; the game board to be played on.

    """
    while True:
        white_player.make_move(game_board)

        if (game_board.winner() is not None) or (game_board.full()):
            return

        black_player.make_move(game_board)

        if (game_board.winner() is not None) or (game_board.full()):
            return

if __name__ == '__main__':
    raise NotImplementedError('The game is yet to be implemented')
