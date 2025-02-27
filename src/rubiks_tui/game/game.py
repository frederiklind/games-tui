import time
from typing import List, Tuple

from cube.rubiks import Cube


class Game(object):
    """
    Maintains game state, including the Cube instance of current game,
    number of moves used, and timer.

    Attributes:
        cube (Cube): Cube instance used for the current game.
        __move_count (int): Number of moves used for the current game.
    """

    __move_count: int
    __max_hist_len: int
    __history: List[Tuple[int, int]]
    cube: Cube

    def __init__(self) -> None:
        """
        creates a new instance of a Rubik's game
        """
        self.__move_count = 0
        self.cube = Cube()

    def increment_move_count(self) -> None:
        """
        Increments the number of moves used for the game.
        """
        self.__move_count += 1

    def restart(self) -> None:
        """
        Resets the game state
        """
        self.__move_count = 0
        self.__history = []
        self.cube = Cube()

