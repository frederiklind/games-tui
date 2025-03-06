from typing import List


class Enemy(object):
    """

    """
    
    health: int

    def __init__(self, health: int) -> None:
        """

        """
        self.health = health

    def __str__(self) -> str:
        return self.__symbol


class DefenseBunker(object):
    """

    """

    blocks: List[List[str]] 
    health: List[List[int]]

    def block(cls, n: int) -> str:
        pass

    def __init__(self) -> None:
        """

        """
        self.blocks = [
            ["█"],
            ["██", "██", "██"],
        ]
        
        # initialize health for each bunker block

        self.health = [[2 for _ in range(4)] for _ in range(2)]  
    
    
    def take_damage(self, x: int) -> bool:
        pass
        




class SpaceInvadersGame(object):
    """

    """

    level: int
    health: int
    enemies: List[List[int]]

    def __init__(self) -> None:
        """

        """
        
        self.level = 1
        self.health = 100


