#! /usr/bin/env python

try:
    import Tkinter as tk # python 2
except ImportError:
    import tkinter as tk # python 3
import lib

def play_game(white_player, black_player, game_board):
    """
    Play a game of gomoku.

    :param white_player, black_player:

        The players that shall play the game as defined in ``lib.player``

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
    board = lib.board.Board(16,9)
    window = tk.Tk()
    gui = lib.gui.BoardGui(board, window)
    player1 = lib.player.Human(lib.board.white, gui)
    player2 = lib.player.Human(lib.board.black, gui)
    play_game(player1, player2, board)
    gui.renew_board()
    print('End of game')
    window.mainloop()
    raise NotImplementedError('The game is yet to be implemented')
