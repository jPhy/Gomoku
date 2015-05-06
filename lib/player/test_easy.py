"Unit tests for the Random player"

from .lib import black, white, empty, PlayerTest
from .easy import *

class TestEasy(PlayerTest):
    Player = Easy
    def setUp(self):
        np.random.seed(42425243212)
