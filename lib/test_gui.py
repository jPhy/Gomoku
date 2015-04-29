import unittest
import numpy as np
from .gui import *

class TestOptionsDialog(unittest.TestCase):
    def test_io(self):
        dialog = OptionsDialog(0,0) # Index zero for human players

        output_getter = dialog.get_players()
        target_output = (0,0)

        np.testing.assert_equal(output_getter, target_output)
