import curses
import time

from ui.window import Window
from games.chess.chess import ChessGame


class ChessUI(Window):
    """
    The chess game UI window.

    Attributes:
        win (curses.window): The curses window of the chess UI.
        game (ChessGame): A game of chess, which is a game, which is good.
    """
    win: "curses.window"
    game: ChessGame

    def __init__(self, stdscr, width, height) -> None:
        super().__init__(stdscr, width, height, idx=0, render_win=True)
        self.render_board()
        
        self.run()


    def render_board(self) -> None:
        """
        Renders the chessboard
        """
        sy = 1

        for r in range(8):
            sx = 3 if r % 2 == 0 else 8
            for c in range(4):
                self.win.addstr(sy, sx, "     ", curses.color_pair(14))     
                self.win.addstr(sy + 1, sx, "     ", curses.color_pair(14))     
                self.win.addstr(sy + 2, sx, "     ", curses.color_pair(14))
                self.win.addstr(sy + 1, sx + 7, "󰡗", curses.color_pair(1))
                sx += 10
            sy += 3
        self.win.refresh()

    def render_pieces(self) -> None:
        pass
        
    def run(self) -> None:
        while True:
            key = self.stdscr.getch()
            if key == ord("q"):
                break



            


