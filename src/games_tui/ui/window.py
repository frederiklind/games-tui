import curses
import time

from enum import Enum
from typing import Optional, Tuple, List, Any, Callable


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
        render_win: Optional[bool] = False
    ) -> None:
        """
        Initializes the component

        Args:
            stdscr (curses stuff): ...
            height (int): height of the window.
            width (int): Width of the window.
            idx (Optional[int]): Start index for the window.
            opts (Optional[List[str]]): List of seletable options.
            render_win (Optional[bool]): Whether to render window on initialization.
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

    def adjust_maxyx(
            self, 
            after: Callable[..., None], 
            render_win: Optional[bool] = False
    ) -> None:
        """
        Adjusts the max yx values of the window if the window have resized.
        Clears the screen and executes the after function if given in 
        the function arguments.

        Args:
            after (Callable[..., None]): Function to execute after clearing the screen.
            render_win (Optional[bool]): Whether to render the window. False by default.
        """
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.max_y, self.max_x) != (max_y, max_x):
            self.max_y = max_y
            self.max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()

            # prevent application crash if window is too small:

            if self. max_y < self.height or self.max_x < self.width:
                msg = "Window is currently too small"
                self.stdscr.addstr(3, 3, msg)
                self.stdscr.refresh()

                while self.max_y < self.height or self.max_x < self.width:
                    self.stdscr.refresh()
                    self.max_y, self.max_x = self.stdscr.getmaxyx()

            if render_win:
                self.render_win()

            after()     # do whatever


    def center_win(self) -> Tuple[int, int]:
        """
        Gets the yx center coordinates of the window.

        Returns:
            Tuple[int, int]: The y and x center coordinates.
        """
        y = self.height // 2
        x = self.width // 2

        return (y, x)

    
    def center_scr(self) -> Tuple[int, int]:
        """
        Gets the yx center coordinates of the stdscr.

        Returns:
            Tuple[int, int]: The y and x center coordinates.
        """
        y = self.max_y // 2
        x = self.max_x // 2

        return (y, x)


    def win_syx(self) -> Tuple[int, int]:
        """
        Gets appropriate start yx coordinates for the window

        Returns:
            Tuple[int, int]: The s_yx coordinates for the window. 
        """
        y = self.max_y // 2 - self.height // 2
        x = self.max_x // 2 - self.wifth // 2

        return (y, x)
