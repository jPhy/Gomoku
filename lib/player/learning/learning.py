from .. import Player, InvalidMoveError
from ..lib import black, white, empty
from os import path
import numpy as np

def dump_log(filename, old_log, new_log):
    filepath = path.join(path.split(__file__)[0], filename)
    new_log = [tuple(item) for item in new_log]
    with open(filepath, 'w') as f:
        f.write('log=')
        f.write(repr(old_log + [new_log]))

def load_oldlog(filename):
    filepath = path.join(path.split(__file__)[0], filename)
    try:
        with open(filepath, 'r') as f:
            exec(f.read())
            return locals()['log']
    except IOError:
        print('        WARNING: "' + filepath + '" not found')
        return []

def reduce_log(log):
    """
    Cut the height and width of the board such that at least one stone is
    placed on each boundary.
    Return the reduced log.

    """
    log = np.array(log)

    x = log[:,0]
    y = log[:,1]

    x -= x.min()
    y -= y.min()

    return log

def make_board(log):
    board = np.zeros((log[:,0].max() + 1 , log[:,1].max() + 1))

    in_turn = white # white begins
    for pos in log:
        board[tuple(pos)] = in_turn
        in_turn *= -1

    return board

def match_log(oldlog, newlog):
    """
    Return the index ``i`` such that oldlog[i - 1] matches newlog (up to
    ``reduce_log()`` and oldlog[i] is the move the opponent has taken
    towards winning.
    If no match is found, return None

    """
    assert empty == 0

    oldlog = np.array(oldlog)
    newlog = np.array(reduce_log(newlog))

    new_board = make_board(newlog)

    for i in range(1, len(oldlog) + 1):
        current_oldlog = reduce_log(oldlog[:i])
        old_board = make_board(current_oldlog)
        if old_board.shape == new_board.shape and (old_board == new_board).all():
            return i

def remove_offset(oldlog, newlog):
    """
    If two logs match up to the ``reduce_offset()``, this function
    undoes the cut in oldlog such that it matches newlog.
    Return oldlog[len(newlog)] from the uncut oldlog; i.e. the move to be
    taken when preventing a previous mistake.

    """
    newlog = np.array(newlog)
    oldlog = np.array(oldlog[:len(newlog) + 2])
    assert len(oldlog) == len(newlog) + 2, "Have len(oldlog) = " + str(len(oldlog)) + ", len(newlog) = " + str(len(newlog))

    new_board = make_board(newlog)
    reduced_board = make_board(oldlog[:-2])

    x_offset = new_board.shape[0] - reduced_board.shape[0]
    y_offset = new_board.shape[1] - reduced_board.shape[1]

    return oldlog[-1][0] + x_offset , oldlog[-1][1] + y_offset

class Learning(Player):
    name = 'Adaptive'
    def __init__(self, *args, **kwargs):
        self.white_logfile = kwargs.pop('white_logfile', "white.log")
        self.black_logfile = kwargs.pop('black_logfile', "black.log")
        self.check_oldlogs = True

        super(Learning, self).__init__(*args, **kwargs)

        self.logfile = self.white_logfile if self.color == white else self.black_logfile
        self.reload_oldlogs()

    def reload_oldlogs(self):
        self.oldlogs = load_oldlog(self.white_logfile) if self.color == white else load_oldlog(self.black_logfile)

    def _make_move(self, gui):
        def place_stone():
            if self.win_if_possible(gui): return
            if self.stop_old_mistake(gui): return
            if self.block_open_four(gui): return
            if self.extend_three_to_doubly_open_four(gui): return
            if self.block_to_doubly_open_four(gui): return
            if self.block_doubly_open_three(gui): return
            if self.block_twice_to_three_or_more(gui): return
            if self.extend_three_to_four(gui): return
            if self.block_open_three(gui): return
            if self.extend_twice_two_to_three(gui): return
            if self.block_doubly_open_two(gui): return
            if self.block_open_two(gui): return
            if self.extend_two_to_three(gui): return
            try:
                gui.board[gui.board.height // 2, gui.board.width // 2] = self.color; return
            except InvalidMoveError:
                try:
                    gui.board[gui.board.height // 2 + 1, gui.board.width // 2] = self.color; return
                except InvalidMoveError:
                    if self.extend_one(gui): return
                    self.random_move(gui)

        place_stone()

        if self.check_oldlogs:
            move_to_make_opponent_win = self.get_move_to_make_opponent_win(gui)
            if move_to_make_opponent_win is not None:
                dump_log(
                            filename = self.logfile,
                            new_log  = reduce_log(gui.board.log + [move_to_make_opponent_win]),
                            old_log  = self.oldlogs
                        )
                self.check_oldlogs = False
                self.reload_oldlogs()

    def get_move_to_make_opponent_win(self, gui):
        """
        Check if a player of opponent color can win the game in the next
        move.
        Return the position where the oppoent has to place a stone to win
        or, if not possible, None.

        """
        opponent_color = -self.color
        opponent_dummy_player = Player(opponent_color)
        return opponent_dummy_player.check_if_immediate_win_possible(gui)

    def stop_old_mistake(self, gui):
        if not self.check_oldlogs:
            return False

        current_log = gui.board.log

        if not self.oldlogs or not current_log:
            return False

        for oldlog in self.oldlogs:
            if match_log(oldlog, current_log):
                # Place stone where opponent would place
                try:
                    next_move = remove_offset(oldlog, current_log)
                    gui.board[next_move] = self.color
                    return True
                except AssertionError:
                    continue
                # raise NotImplementedError("The player 'Adaptive' is not ready to use yet. Choose a different player.")
        return False
