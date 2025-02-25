import json

from Typing import List, Dict
from datetime import datetime


class Result(Object):
    """
    Contains results of a successfully completed game.

    Attributes:
        date (str): Datetime of the game instance.
        move_count (int): Number of moves used for solving a cube.
        elapsed_time (float): Time used for solving a cube.
    """

    date: str
    move_count: int
    elapsed_time: float

class Result(Object):
    """

    """

    move_count: int
    elapsed_time    def __init__(self, date: str, move_count: int, elapsed_time: float) -> None:
        """
        
        """
        self.date = date
        self.move_count = move_count
        self.elapsed_time = elapsed_time

    def to_dict(self) -> dict:
        """
        Converts the Result instance into a dictionary.
        
        Returns:
            
        """
        return {
            "date": self.date,
            "elapsed_time": self.elapsed_time,
            "game_date": self.move_count
        }
    

class Results(Object):
    """

    """
    __results: List[Results]

    def __init__(self) -> None:
    
        pass

    def add(move_count: int, elapsed_time: float) -> None:
        """

        """


