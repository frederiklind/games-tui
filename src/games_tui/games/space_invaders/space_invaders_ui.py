import curses
import time

from collections import deque
from typing import List, Tuple, Optional, Deque
from ui.window import Window
from games.space_invaders.space_invaders import SpaceInvadersGame


class SpaceInvadersUI(Window):
    """
    
    """
    game: SpaceInvadersGame
    
    def __init__(self, stdscr, height: int, width: int) -> None:
        """

        """
        super().__init__(stdscr, height, width, idx=0, render_win=True)
        
        self.game = SpaceInvadersGame()

        self.make_win()
        self.run()

    
    def make_win(self) -> None:
        self.render_stats()
        
        self.win.refresh()

    
    def render_mothership() -> None:
        pass

        
    def render_enemies() -> None:
        pass

    def render_stats(self) -> None:
        self.win.attron(curses.color_pair(2) | curses.A_BOLD)
        self.win.addstr(1, 2, "SCORE:")
        self.win.addstr(1, self.center_x() - 6, "LEVEL:")
        self.win.addstr(1, self.width - 15, "HIGH:")

        
    def run(self) -> None:
        self.stdscr.nodelay(True)
        self.win.timeout(100)

        while True: 
            key = self.stdscr.getch()

            if key == ord("q"):
                break
