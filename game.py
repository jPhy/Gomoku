#! /usr/bin/env python

try:
    # python 2
    import Tkinter as tk
    from tkMessageBox import Message
except ImportError:
    # python 3
    import tkinter as tk
    from tkinter.messagebox import Message
import lib

def play_game(white_player, black_player, game_board):
    """
    Play a game of gomoku.
    Return the winner (or None) and the positions of the line of five.

    :param white_player, black_player:

        The players that shall play the game as defined in ``lib.player``

    :param game_board:

        Instance of ``lib.board.Board``; the game board to be played on.

    """
    while True:
        white_player.make_move(game_board)

        winner, positions = game_board.winner()
        if (winner is not None) or (game_board.full()):
            return winner, positions

        black_player.make_move(game_board)

        winner, positions = game_board.winner()
        if (winner is not None) or (game_board.full()):
            return winner, positions

if __name__ == '__main__':
    board = lib.board.Board(16,13)
    window = tk.Tk()
    window.title('Gomoku')
    gui = lib.gui.BoardGui(board, window)
    player1 = lib.player.Human(lib.board.white, gui)
    player2 = lib.player.Human(lib.board.black, gui)
    winner, positions = play_game(player1, player2, board)
    gui.renew_board()
    gui.highlight_winner(positions)
    if winner == lib.board.white:
        Message(message='White wins!', icon='info', title='Gomoku').show()
    elif winner == lib.board.black:
        Message(message='Black wins!', icon='info', title='Gomoku').show()
    elif winner is None:
        Message(message='Draw!', icon='info', title='Gomoku').show()
    else:
        raise RuntimeError('FATAL ERROR')
