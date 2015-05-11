"Unit tests for the Random player"

from .lib import black, white, empty, PlayerTest
from .hard import *

class TestHard(PlayerTest):
    Player = Hard
    def setUp(self):
        np.random.seed(42425243212)
