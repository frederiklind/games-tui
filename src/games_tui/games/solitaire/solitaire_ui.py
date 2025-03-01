import curses
import time

from ui.window import Window
from games.solitaire.solitaire import SolitaireGame


class SolitaireUI(Window):
    """
    """
    win: "curses.window"
    game: SolitaireGame

    def __init__(self, stdscr, width, height) -> None:
        super().__init__(stdscr, width, height, idx=0, render_win=True)
        
        self.run()


        
    def run(self) -> None:
        while True:
            key = self.stdscr.getch()
            if key == ord("q"):
                break
