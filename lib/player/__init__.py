'Gomoku players'

from __future__ import print_function
from ..board import InvalidMoveError
from .lib import Playerlibrary


# base class
class Player(Playerlibrary):
    """
    Describtion of a player to be used in the Game.
    To implement your own AI, override the function
    ``_make_move``.
    .. important::
        Note the leading underscore. Do *NOT* override ``make_move``.
    The member string ``name`` appears in the options dialog.

    :param color:

        The color that the player plays as described in "board.py".

    """
    name = 'Stupid AI'
    def __init__(self, color):
        self.color = color

    def make_move(self, gui):
        """
        Place a stone onto the `board`.
        This is a common function that *should not be overridden*.
        Override ``_make_move`` instead.

        :param gui:

            The game ``BoardGui`` as described in "gui.py"

        """
        gui.renew_board()
        if hasattr(gui.board, 'lastmove'):
            gui.highlight_lastmove()
        gui.color_in_turn = self.color
        moves_left = gui.board.moves_left

        self._make_move(gui)

        if not gui.in_game:
            return

        if not moves_left - 1 == gui.board.moves_left:
            raise RuntimeError('Could not find any valid move')

    def _make_move(self, gui):
        "Override this function for specific players"
        for i in range(gui.board.height):
            for j in range(gui.board.width):
                try:
                    gui.board[i,j] = self.color
                    return
                except InvalidMoveError:
                    pass


# Human player
class Human(Player):
    """
    A human player using a gui for input.

    :param color:

        The color that the player plays as described in "board.py".

    """
    name = 'Human'
    def _make_move(self, gui):
        # wait for user input
        gui.need_user_input = True
        moves_left = gui.board.moves_left
        while gui.board.moves_left == moves_left and gui.in_game:
            gui.update()
        gui.need_user_input = False



# search for player types in all files of this folder
available_player_types = [Human, Player]
from os import listdir, path
player_directory = path.split(__file__)[0]
print('Searching for players in', player_directory)
filenames = listdir(player_directory)
for filename in filenames:
    if filename[-3:] != '.py' or 'test' in filename or \
       filename == '__init__.py' or filename == 'lib.py':
           continue
    print('Processing', filename)
    exec('from . import ' + filename[:-3] + ' as playerlib')
    # search for classes derived from the base class ``Player``
    for objname in dir(playerlib):
        obj = playerlib.__dict__[objname]
        if type(obj) is not type or obj in available_player_types:
            continue
        if issubclass(obj, Player):
            print('    found', obj.name)
            available_player_types.append(obj)


# player management
available_player_names = [player.name for player in available_player_types]
def get_player_index(name, hint=None):
    """
    Convert the player name into an integer valued index.

    :param name:
        string; the name if the player that is listed in ``available_player_names``

    :param hint:
        integer, optional; the first index do be checked.

    """
    for i,n in enumerate(available_player_names):
        if n == name:
            return i
    # the following is executed if the name is not found
    raise ValueError('"%s" is not a registered player type' % name)
