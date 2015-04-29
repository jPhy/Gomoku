"""
Implement the game's gui

"""

try:
    # python 2
    import Tkinter as tk
    from tkMessageBox import Message
except ImportError:
    # python 3
    import tkinter as tk
    from tkinter.messagebox import Message

from .player import available_player_names, available_player_types, get_player_index

class Window(tk.Tk):
    "Wrapper for the basic window"
    def update(self, *args, **kwargs):
        """
        Extend the base method ``update``.

        Return ``True`` if the window is still open, return ``False``
        if the window has been destroyed.

        """
        try:
            tk.Tk.update(self, *args, **kwargs)
            return True
        except tk.TclError as err:
            if 'has been destroyed' in err.args[0]:
                return False
            else:
                raise err

gui_invalid_move_message = Message(message='Invalid move!', icon='error', title='Gomoku')

import numpy as np
from . import player, board
from .board import black,white,empty , InvalidMoveError

class BoardGui(object):
    """
    Gui of a Gomoku game board. Create a window with buttons
    associated to a game Board (see "board.py")

    :param board:

        The game board for which to create a gui.

    :param window:

        The window to attach the gui to.

    """
    # This is NOT a duplicate from class ``Window``
    # Note that this function has an exit(0), not a return
    def update(self, *args, **kwargs):
        try:
            tk.Canvas.update(self.window, *args, **kwargs)
        except tk.TclError as err:
            if 'has been destroyed' in err.args[0]:
                exit(0)
            else:
                raise err

    def __init__(self, board, window):
        self.board = board
        self.window = window

        self.buttons = np.empty_like(board.board, dtype='object')
        for i in range(self.board.width):
            for j in range(self.board.height):
                current_button = self.buttons[j,i] = tk.Button(window)
                current_button.grid(row=i, column=j)

    def game_running_buttons(self):
        def button_command(i,j):
            try:
                self.board[j,i] = self.board.in_turn
            except InvalidMoveError:
                gui_invalid_move_message.show()

        for i in range(self.board.width):
            for j in range(self.board.height):
                self.buttons[j,i].config( command=lambda x=i, y=j: button_command(x,y) )

    # Note: the variable ``in_game`` is used to break loops that wait for user interactions

    def game_running(self):
        self.in_game = True
        self.game_running_buttons()

    def game_over(self):
        self.in_game = False
        self.game_over_buttons()

    def game_message_buttons(self, message):
        """
        Deactivate the game buttons; show error message ``message`` if pressed.

        """
        def button_command():
            Message(message=message, icon='error', title='Gomoku').show()

        for i in range(self.board.width):
            for j in range(self.board.height):
                self.buttons[j,i].config(command=button_command)

    def game_over_buttons(self):
        self.game_message_buttons('The game is already over!\nStart a new game first.')

    def game_paused_buttons(self):
        self.game_message_buttons('Close the options dialog first.')

    def renew_board(self):
        "Draw the stone symbols onto the buttons"
        for i in range(self.board.width):
            for j in range(self.board.height):
                if self.board[j,i] == black:
                    self.buttons[j,i].config(background='black', activebackground='black', highlightthickness=3, highlightbackground='lightgray')
                elif self.board[j,i] == white:
                    self.buttons[j,i].config(background='white', activebackground='white', highlightthickness=3, highlightbackground='lightgray')
                elif self.board[j,i] == empty:
                    self.buttons[j,i].config(background='darkgray', activebackground='darkgray', highlightthickness=3, highlightbackground='lightgray')

    def highlight_winner(self, positions):
        """
        Highlight the buttons with the coordinates ``(y,x)``
        (see board.py) passed via ``positions``

        :param positions:
            iterable if tuples with the coordinates as specified in
            'board.py'

        """
        for y,x in positions:
            self.buttons[y,x].config(highlightbackground='red')

    def highlight_lastmove(self):
        """
        Highlight the button with the coordinates of the last move.

        """
        self.buttons[self.board.lastmove].config(highlightbackground='yellow')

class MainWindow(Window):
    """
    Gui of Gomoku; the main window.

    :param width, height:

        width and height of the Gomoku game board

    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        Window.__init__(self)
        self.title('Gomoku')

        self.canvas_board = tk.Canvas(self)
        self.canvas_board.pack()

        self.board = board.Board(self.width,self.height)
        self.gui = BoardGui(self.board, self.canvas_board)

        self.canvas_controls = tk.Canvas(self)
        self.canvas_controls.pack(side='bottom')
        self.new_game_button = tk.Button(self.canvas_controls, text='New game')
        self.new_game_button.grid(column=0, row=0)
        self.options_button = tk.Button(self.canvas_controls, text='Options')
        self.options_button.grid(column=1, row=0)
        self.exit_button = tk.Button(self.canvas_controls, text='Exit')
        self.exit_button.grid(column=2, row=0)
        self.activate_buttons()

        self.start_new_game = True

        # set the players
        # white_player = player.Human(board.white)
        # self.white_player = player.Player(board.white)
        # black_player = player.Human(board.black)
        # self.black_player = player.Player(board.black)
        self.white_player_idx = self.black_player_idx = 1

    def mainloop(self):
        # run until the user exits the program
        while True:
            # Start a new game only if desired by user.
            # This bootstrap prevents the deletion of the old game board
            # until the user presses the 'New game' button.
            while not self.start_new_game:
                if not self.update():
                    return
            self.start_new_game = False
            self.play_game()

    def new_game(self): # button command
        self.gui.game_over()
        self.start_new_game = True

    def play_game(self):
        "Run a game of gomoku"
        # enter "in_game" mode
        self.gui.game_running()

        # remove all stones from the board
        self.board.reset()
        self.gui.renew_board()

        white_player = available_player_types[self.white_player_idx](white)
        black_player = available_player_types[self.black_player_idx](black)

        while True:
            white_player.make_move(self.gui)
            if not self.gui.in_game:
                # game aborted
                return
            self.gui.update()

            winner, positions = self.board.winner()
            if (winner is not None) or (self.board.full()):
                break

            black_player.make_move(self.gui)
            if not self.gui.in_game:
                # game aborted
                return
            self.gui.update()

            winner, positions = self.board.winner()
            if (winner is not None) or (self.board.full()):
                break

        self.gui.renew_board()
        self.gui.highlight_winner(positions)
        if not self.gui.in_game:
            # game aborted
            return
        elif winner == white:
            Message(message='White wins!', icon='info', title='Gomoku').show()
        elif winner == black:
            Message(message='Black wins!', icon='info', title='Gomoku').show()
        elif winner is None:
            Message(message='Draw!', icon='info', title='Gomoku').show()
        else:
            raise RuntimeError('FATAL ERROR')

        # end "in_game" mode
        self.gui.game_over()

    def buttons_option_mode(self):
        def new_game_button_command():
            Message(message='Close the options dialog first.', icon='error', title='Gomoku').show()

        def options_button_command():
            Message(message='The options dialog is already open!', icon='error', title='Gomoku').show()

        self.gui.game_paused_buttons()
        self.new_game_button.config(command=new_game_button_command)
        self.options_button.config(command=options_button_command)
        self.exit_button.config(command=self.destroy)

    def activate_buttons(self):
        self.gui.game_running_buttons()
        self.new_game_button.config(command=self.new_game)
        self.options_button.config(command=self.options)
        self.exit_button.config(command=self.destroy)

    def options(self): # button command
        self.buttons_option_mode()

        options_dialog = OptionsDialog(self.white_player_idx, self.black_player_idx)
        while options_dialog.update():
            try:
                self.state()
            except tk.TclError as err:
                if 'has been destroyed' in err.args[0]:
                    options_dialog.destroy()
                    return
                raise err

        self.white_player_idx , self.black_player_idx = options_dialog.get_players()

        self.activate_buttons()
        if not self.gui.in_game:
            self.gui.game_over()

class OptionsDialog(Window):
    """
    Show a dialog to set the game options.
    Return a dictionary of options.

    """
    def __init__(self, current_white_player_index, current_black_player_index):
        Window.__init__(self)
        self.title('Gomoku - Options')

        self.previous_white_player_index = current_white_player_index
        self.previous_black_player_index = current_black_player_index

        width = 250
        height = 10

        self.topspace = tk.Canvas(self, height=height, width=width)
        self.topspace.pack()

        player_width  = 100
        player_height =  20

        self.cv_options = tk.Canvas(self)
        self.cv_options.pack()

        self.canvas_white_player = tk.Canvas(self.cv_options, width=player_width, height=player_height)
        self.canvas_white_player.create_text(40,10, text='white player')
        self.canvas_white_player.grid(column=0,row=0)
        self.desired_white_player = tk.Variable(value=available_player_names[current_white_player_index])
        self.dialog_white_player = tk.OptionMenu(self.cv_options, self.desired_white_player, *available_player_names)
        self.dialog_white_player.grid(column=1,row=0)

        self.canvas_black_player = tk.Canvas(self.cv_options, width=player_width, height=player_height)
        self.canvas_black_player.create_text(40,10, text='black player')
        self.canvas_black_player.grid(column=0,row=1)
        self.desired_black_player = tk.Variable(value=available_player_names[current_black_player_index])
        self.dialog_black_player = tk.OptionMenu(self.cv_options, self.desired_black_player, *available_player_names)
        self.dialog_black_player.grid(column=1,row=1)

        self.middlespace = tk.Canvas(self, height=height+5, width=width)
        self.middlespace.pack()

        self.button_close = tk.Button(self, text='Done', command=self.destroy)
        self.button_close.pack()

        self.bottomspace = tk.Canvas(self, height=height, width=width)
        self.bottomspace.pack()

    def get_players(self):
        "Return the indices of the desired white and black player."
        white_player_idx = get_player_index(self.desired_white_player.get(), hint=self.previous_white_player_index)
        black_player_idx = get_player_index(self.desired_black_player.get(), hint=self.previous_black_player_index)
        return (white_player_idx,black_player_idx)
