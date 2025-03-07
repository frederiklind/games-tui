import time

from typing import List, Tuple, Deque 
from collections import deque


class RubiksCube(object):
    """
    Object representation of the Rubik's cube. Maintains the state of
    the faces, and performs the different rotations on the cube.

    Attributes:
        __cube: (List[List[List[int]]]): 3 dimensional list for storing color indices
    """

    __cube: List[List[List[int]]]

    def __init__(self):
        """
        Initializes a new instance of a Rubik's cube in a solved state.
        """
        self.__cube = [[[i for _ in range(3)] for _ in range(3)] for i in range(6)]
    
    def is_valid(self) -> bool:
        for i in range(6):
            color = self.__cube[i][0][0]
            for row in self.__cube[i]:
                if any(cell != color for cell in row):
                    return False
        return True

    def __rotate_top(self, direction: int) -> None:
        """
        Rotates top (white) face of the cube.

        Args:
            direction (int): Binary representation of the direction of rotation.
        """
        if direction == 0:
            self.__cube[0] = [list(row) for row in zip(*self.__cube[0][::-1])]
            temp = self.__cube[4][0][:]
            for j in range(3):
                self.__cube[4][0][j] = self.__cube[3][0][j]
                self.__cube[3][0][j] = self.__cube[5][0][j]
                self.__cube[5][0][j] = self.__cube[2][0][j]
                self.__cube[2][0][j] = temp[j]
        elif direction == 1:
            self.__cube[0] = [list(row) for row in zip(*self.__cube[0])][::-1]
            temp = self.__cube[4][0][:]
            for j in range(3):
                self.__cube[4][0][j] = self.__cube[2][0][j]
                self.__cube[2][0][j] = self.__cube[5][0][j]
                self.__cube[5][0][j] = self.__cube[3][0][j]
                self.__cube[3][0][j] = temp[j]
        else:
            return

    def __rotate_bottom(self, direction: int) -> None:
        """

        """
        if direction == 0:
            self.__cube[1] = [list(row) for row in zip(*self.__cube[1][::-1])]
            temp = self.__cube[4][2][:]
            for j in range(3):
                self.__cube[4][2][j] = self.__cube[2][2][j]
                self.__cube[2][2][j] = self.__cube[5][2][j]
                self.__cube[5][2][j] = self.__cube[3][2][j]
                self.__cube[3][2][j] = temp[j]
        elif direction == 1:
            self.__cube[1] = [list(row) for row in zip(*self.__cube[1])][::-1]
            temp = self.__cube[4][2][:]
            for j in range(3):
                self.__cube[4][2][j] = self.__cube[3][2][j]
                self.__cube[3][2][j] = self.__cube[5][2][j]
                self.__cube[5][2][j] = self.__cube[2][2][j]
                self.__cube[2][2][j] = temp[j]
        else:
            return

    def __rotate_left(self, direction: int) -> None:
        """

        """
        if direction == 0:
            self.__cube[2] = [list(row) for row in zip(*self.__cube[2][::-1])]
            temp = [self.__cube[0][r][0] for r in range(3)]
            for r in range(3):
                self.__cube[0][r][0] = self.__cube[4][r][0]
            for r in range(3):
                self.__cube[4][r][0] = self.__cube[1][r][0]
            for r in range(3):
                self.__cube[1][r][0] = self.__cube[5][2 - r][2]
            for r in range(3):
                self.__cube[5][r][2] = temp[2 - r]
        elif direction == 1:
            self.__cube[2] = [list(row) for row in zip(*self.__cube[2])][::-1]
            temp = [self.__cube[0][r][0] for r in range(3)]
            for r in range(3):
                self.__cube[0][r][0] = self.__cube[5][r][2]
            for r in range(3):
                self.__cube[5][r][2] = self.__cube[1][2 - r][0]
            for r in range(3):
                self.__cube[1][r][0] = self.__cube[4][r][0]
            for r in range(3):
                self.__cube[4][r][0] = temp[r]
        else:
            return

    def __rotate_right(self, direction: int) -> None:
        """

        """
        if direction == 0:
            self.__cube[3] = [list(row) for row in zip(*self.__cube[3][::-1])]
            temp = [self.__cube[0][r][2] for r in range(3)]
            for r in range(3):
                self.__cube[0][r][2] = self.__cube[4][r][2]
            for r in range(3):
                self.__cube[4][r][2] = self.__cube[1][r][2]
            for r in range(3):
                self.__cube[1][r][2] = self.__cube[5][2 - r][0]
            for r in range(3):
                self.__cube[5][r][0] = temp[2 - r]

        elif direction == 1:
            self.__cube[3] = [list(row) for row in zip(*self.__cube[3])][::-1]
            temp = [self.__cube[0][r][2] for r in range(3)]
            for r in range(3):
                self.__cube[0][r][2] = self.__cube[5][r][0]
            for r in range(3):
                self.__cube[5][r][0] = self.__cube[1][2 - r][2]
            for r in range(3):
                self.__cube[1][r][2] = self.__cube[4][r][2]
            for r in range(3):
                self.__cube[4][r][2] = temp[r]
        else:
            return

    def __rotate_front(self, direction: int) -> None:
        """

        """
        if direction == 0:
            self.__cube[4] = [list(row) for row in zip(*self.__cube[4][::-1])]
            temp = [self.__cube[0][2][i] for i in range(3)]
            for i in range(3):
                self.__cube[0][2][i] = self.__cube[2][2 - i][2]
                self.__cube[2][2 - i][2] = self.__cube[1][0][2 - i]
                self.__cube[1][0][2 - i] = self.__cube[3][i][0]
                self.__cube[3][i][0] = temp[i]
        elif direction == 1:
            self.__cube[4] = [list(row) for row in zip(*self.__cube[4])][::-1]
            temp = [self.__cube[0][2][i] for i in range(3)]
            for i in range(3):
                self.__cube[0][2][i] = self.__cube[3][i][0]
                self.__cube[3][i][0] = self.__cube[1][0][2 - i]
                self.__cube[1][0][2 - i] = self.__cube[2][2 - i][2]
                self.__cube[2][2 - i][2] = temp[i]
        else:
            return

    def __rotate_back(self, direction: int) -> None:
        """

        """
        if direction == 0:
            self.__cube[5] = [list(row) for row in zip(*self.__cube[5][::-1])]
            temp = [self.__cube[0][0][i] for i in range(3)]
            for i in range(3):
                self.__cube[0][0][i] = self.__cube[3][i][2]
                self.__cube[3][i][2] = self.__cube[1][2][2 - i]
                self.__cube[1][2][2 - i] = self.__cube[2][2 - i][0]
                self.__cube[2][2 - i][0] = temp[i]
        elif direction == 1:
            self.__cube[5] = [list(row) for row in zip(*self.__cube[5])][::-1]
            temp = [self.__cube[0][0][i] for i in range(3)]
            for i in range(3):
                self.__cube[0][0][i] = self.__cube[2][2 - i][0]
                self.__cube[2][2 - i][0] = self.__cube[1][2][2 - i]
                self.__cube[1][2][2 - i] = self.__cube[3][i][2]
                self.__cube[3][i][2] = temp[i]
        else:
            return

    def rotate(self, face: int, direction: int) -> bool:
        """
        Main rotate function for performing moves on the cube instance.
        Takes face index, and number representation of the derection of
        which the specified face must rotate (0: clock, 1: counter clock).
        This matches the face index with the correct rotation function.

        Args:
           face (int): The index of the cube face to be rotated.
           direction (int): The binary value for direction of rotation.
        """
        match face:
            case 0:
                self.__rotate_top(direction)
            case 1:
                self.__rotate_bottom(direction)
            case 2:
                self.__rotate_left(direction)
            case 3:
                self.__rotate_right(direction)
            case 4:
                self.__rotate_front(direction)
            case 5:
                self.__rotate_back(direction)
            case _:
                raise Exception("Invalid face index")
        return self.is_valid()


    def get(self) -> List[List[List[int]]]:
        """

        """
        return self.__cube


class RubiksGame(object):
    """
    Maintains game state, including the Cube instance of current game,
    number of moves used, and timer.

    Attributes:
        num_moves (int): Number of moves used for the current game.
        history: (Deque[Tuple[int, int]]): Double ended queue for storing previous moves.
    """
    cube: RubiksCube 
    num_moves: int
    history: Deque[Tuple[int, int]]
    __time: float

    def __init__(self) -> None:
        """
        Initializes an instance of a Rubik's game, with an initial move count
        of 0, and an empty history queue.
        """
        self.cube = RubiksCube()
        self.num_moves = 0
        self.history = deque()
        self.__time = time.time()

    def add(self, face: int, direction: int) -> None:
        """
        Increments the number of moves used for the game, and adds the tuple
        of the history queue
        """
        self.num_moves += 1
        self.history.append((face, direction))
        if len(self.history) > 100:
            self.history.popleft()

    def revert_move(self) -> bool:
        """
        Reverts the last move on the cube.
        """
        if self.history:
            last_move = self.history.pop()
            face, direction = last_move
            reverse_direction = 1 if direction == 0 else 0
            self.cube.rotate(face, reverse_direction)
            self.num_moves += 1  
            return True
        return False
    
    def move(self, face: int, direction: int) -> bool:
        return self.cube.rotate(face, direction)

    def time(self):
        return self.__time

    def set_time(self, time) -> None:
        """
        Sets the game time to whatever time.

        Args:
            time (sometime): Any time.
        """
        self.__time = time

    def get_cube(self) -> List[List[List[str]]]:
        return self.cube.get()
