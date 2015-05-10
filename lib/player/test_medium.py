"Unit tests for the Random player"

from .lib import black, white, empty, PlayerTest
from .medium import *

class TestMedium(PlayerTest):
    Player = Medium
    def setUp(self):
        np.random.seed(42425243212)
