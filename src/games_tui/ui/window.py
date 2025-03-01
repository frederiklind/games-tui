import curses

from enum import Enum
from typing import Optional, List, Any


class Window:
    """
    Base class for windows.
    """

    height: int
    width: int
    max_x: int
    max_y: int
    idx: Optional[int]
    opts: Optional[List[Any]]
    win: "curses.window"

    def __init__(
        self, 
        stdscr, 
        height: int, 
        width: int, 
        idx: Optional[int] = None,
        opts: Optional[List[Any]] = None,
        render_win=False
    ) -> None:
        """
        Initializes the component
        """
        self.stdscr = stdscr
        self.height = height
        self.width = width 
        
        max_y, max_x = self.stdscr.getmaxyx()
        self.max_y = max_y
        self.max_x = max_x
        self.idx = idx
        self.opts = opts

        if render_win:
            self.render_win()

    def render_win(self) -> None:
        self.stdscr.clear()
        self.stdscr.refresh()
        sy = self.max_y // 2 - self.height // 2
        sx = self.max_x // 2 - self.width // 2
        self.win = curses.newwin(self.height, self.width, sy, sx) 
        self.win.bkgd(" ", curses.color_pair(7))
        self.win.refresh()
        self.stdscr.refresh()

