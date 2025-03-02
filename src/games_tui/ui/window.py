import curses

from enum import Enum
from typing import Optional, List, Any, Callable


class Window:
    """
    Base class for windows.

    Attributes:
        height (int): The height of the window. 
        width (int): The width of the window.
        max_y (int): The max y value of the curses standard screen.
        max_x (int): The max x value of the curses standard screen.
        idx (int): The current index of the selected item.
        opts (List[str]): The selectable options of the window.
        win (curses.window): The curses window component. 
    """

    height: int
    width: int
    max_y: int
    max_x: int
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
        """
        Renders the window on screen.
        """
        self.stdscr.clear()
        self.stdscr.refresh()
        sy = self.max_y // 2 - self.height // 2
        sx = self.max_x // 2 - self.width // 2
        self.win = curses.newwin(self.height, self.width, sy, sx) 
        self.win.bkgd(" ", curses.color_pair(7))
        self.win.refresh()
        self.stdscr.refresh()

    def adjust_maxyx(self, after: Callable[..., None]) -> None:
        """
        Adjusts the max yx values of the window if the window have resized.
        Clears the screen and executes the after function if given in 
        the function arguments.

        Args:
            after (Callable[..., None]): Function to execute after clearing the screen.
        """
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.max_y, self.max_x) != (max_y, max_x):
            self.max_y = max_y
            self.max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()

            after()     # do whatever
