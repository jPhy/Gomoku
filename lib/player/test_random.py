"Unit tests for the Random player"

from .lib import black, white, empty, PlayerTest
from .random import *

class TestRandomPlayer(PlayerTest):
    Player = Random
    def setUp(self):
        np.random.seed(42425243212)
