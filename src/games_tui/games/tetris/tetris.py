import random

from typing import List


class Block(object):
    """

    """
    def __init__(self) -> None:
        pass

    def image(self) -> None:
        pass

    def rotate(self) -> None:
        pass


class Tetris(object):
    """
    Tetris game class.

    Attributes:
        some attr:
        ...
    """
    shapes: List[List[List[int]]] 
    level = 1
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    zoom = 20
    y = 60
    x = 100
    block = None
    next_block = None


    def __init__(self) -> None:
        """

        """
        pass
