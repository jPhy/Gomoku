"Unit tests for the Random player"

from ..lib import black, white, empty, PlayerTest
from .learning import *

class TestLearning(PlayerTest):
    Player = Learning

    def remove_logfile(self):
        from os import remove, path
        try:
            remove( path.join(path.split(__file__)[0], self.logfile_name) )
        except OSError:
            # nothing to do if file does not exist
            pass

    def tearDown(self):
        self.remove_logfile()

    def setUp(self):
        self.logfile_name = 'test_adaptive.log'
        self.remove_logfile()
        np.random.seed(42425243212)

    def test_match_log(self):
        self.assertEqual( match_log([(1,2),(3,4)]       , [(1,2),(3,4)]) , 2)
        self.assertEqual( match_log([(1,2),(3,4)]       , [(0,0),(2,2)]) , 2)
        self.assertEqual( match_log([(1,2),(3,4),(9,99)], [(0,0),(2,2)]) , 2)
        self.assertEqual( match_log([(1,3),(3,4)]       , [(0,0),(2,2)]) , None)

        self.assertEqual( match_log([(1,2),(9,3),(3,4)], [(1,1),(3,3),(9,2)]) , None) # wrong colors !!
        self.assertEqual( match_log([(9,3),(3,4),(1,2)], [(1,1),(3,3),(9,2)]) , 3)

    def test_remove_offset(self):
        self.assertEqual( remove_offset([(1,2),(3,4),(1,1),(9,99)], [(0,0),(2,2)]) , (8,97))
        self.assertEqual( remove_offset([(9,3),(3,4),(1,2),(111,111),(10,10)], [(1,1),(3,3),(9,2)]) , (10,9))
        self.assertEqual( remove_offset([(6,1),(0,2),(7,0),(111,111),(7,8)], [(10,1),(3,3),(9,2)]) , (10,9))

        self.assertRaises(AssertionError, remove_offset, [(6,1),(0,2),(7,0),(7,8)], [(10,1),(3,3),(9,2)] )

    def base_test(self):
        class DummyPlayer(Player):
            def __init__(self, *args, **kwargs):
                Player.__init__(self, *args, **kwargs)
                self.i = 0

            def _make_move(self, gui):
                gui.board[log[self.i]] = self.color
                self.i += 2

        log = [(5, 7), (6, 8), (4, 6), (3, 5), (5, 5), (3, 7), (6, 6), (5, 6), (7, 5), (4, 8),
               (6, 4), (6, 5), (8, 4), (9, 3), (7, 3), (8, 2), (7, 4), (5, 4), (7, 6), (7, 2), (7, 7)]

        # first game, white (DummyPlayer) should win
        adaptive_player1 = Learning(color=black, white_logfile='', black_logfile=self.logfile_name)
        dummy_player1 = DummyPlayer(white)
        gui1 = self.build_gui(np.zeros((13,16)))
        for i in range(len(log)):
            if i % 2: # if ``i`` is odd
                adaptive_player1.make_move(gui1)
            else: # if ``i`` is even
                dummy_player1.make_move(gui1)
            self.assertEqual(gui1.board.lastmove, log[i])
            if i != len(log) - 1:
                self.assertTrue(gui1.board.winner()[0] is None)
            else:
                self.assertEqual(gui1.board.winner()[0], white)

        # second game, the Learning player should place its first stone at log[2]
        adaptive_player2 = Learning(color=black, white_logfile='', black_logfile=self.logfile_name)
        dummy_player2 = DummyPlayer(white)
        gui2 = self.build_gui(np.zeros((13,16)))

        dummy_player2.make_move(gui2)
        self.assertEqual(gui2.board.lastmove, log[0])
        self.assertTrue(gui2.board.winner()[0] is None)

        adaptive_player2.make_move(gui2)
        self.assertNotEqual(gui2.board.lastmove, log[1]) # ``Learning``'s move differs from first game?
        self.assertEqual(gui2.board.lastmove, log[2])
