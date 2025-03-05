import unittest
import copy
import random
from src.games_tui.games.rubiks.rubiks import RubiksCube, RubiksGame 


class TestRubiksCube(unittest.TestCase):
    def setUp(self):
        """
        Initialize a Rubik's cube instance before tests.
        """
        self.cube = RubiksCube()

    def test_rotation(self):
        """
        Test rotating the top face clockwise.
        """
        initial_state = copy.deepcopy(self.cube.get())
        self.cube.rotate(5, 1)
        self.assertNotEqual(initial_state, self.cube.get())
        

class TestRubiksGame(unittest.TestCase):
    def setUp(self):
        """
        Initialize a Rubik's game instance before tests.
        """
        self.game = RubiksGame()


if __name__ == "__main__":
    unittest.main()


