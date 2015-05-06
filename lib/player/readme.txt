Tutorial how to implement an AI
===============================

1.  Create a new file (filename is arbitrary) in this folder that contains
    one or more classes derived from Player. The name of your AI that shall
    be displayed in the gui is set by the member variable ``name``:
    >>> class MyAI(Player):
    ...     name = "my AI's name"

    Use the statement ``from . import Player``.
    Override the member function ``_make_move(self, gui)``.
    **********************************************************************
    * IMPORTANT: Note the underscore! Do NOT override ``make_move(...)`` *
    *            without underscore.                                     *
    **********************************************************************
    To place a stone of the own color at (i,j) use the statement
    ``gui.board[i,j] = self.color``.
    You can check the color your player is demanded to play as
    ``self.color == black/white`` where black and white (and ``empty``)
    are to be imported as ``from ..board import black, white, empty``.
    The boards already lying on the board can be accessed via
    ``gui.board[i,j] == black/white/empty``. In addition, there
    are functions like get_line, get_column, ... (see class ``Board``).
    The full board as numpy array is available via ``gui.board.board``.
    Note that black, white and empty are defined as +1, -1 and 0
    such that you can e.g. check if there is an empty position by
    ``<>.prod() == 0``. Furthermore, you can check if a field is occupied
    by your opponent using ``gui.board[i,j] == - self.color``.
    Common subroutines are available as member functions. You can (and
    this should always be the first call of an intelligent AI) e.g.
    check if the AI can win the game in the current turn by calling
    ``self.win_if_possible()`` (see docstring of class .lib.Playerlib).

2.  It is not mandatory but highly recommended to write unit tests for
    your AI. In order to do so, create a sencond file whose name is
    "test_<ai_filename>" where <ai_filename> is the file containing the
    Player class. Import the testing tool kit by
    ``from .lib.testtools import empty, black, white, PlayerTest``.
    To test your AI, create a subclass of ``PlayerTest``, set
    the class variable Player = <Your AI player> and refer to the docstring
    of PlayerTest as well as to built-in AIs for further help.
