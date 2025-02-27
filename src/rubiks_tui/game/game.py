import time
from typing import List, Tuple

from cube.rubiks import Cube


class Game(object):
    """
    Maintains game state, including the Cube instance of current game,
    number of moves used, and timer.

    Attributes:
        cube (Cube): Cube instance used for the current game.
        num_moves (int): Number of moves used for the current game.
    """

    num_moves: int
    history: List[Tuple[int, int]]
    __max_hist_len: int

    def __init__(self) -> None:
        """

        """
        self.num_moves = 0
        self.cube = Cube()

    def increment_move_count(self) -> None:
        """
        Increments the number of moves used for the game.
        """
        self.num_moves += 1



