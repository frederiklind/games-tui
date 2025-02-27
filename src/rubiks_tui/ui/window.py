import curses

from typing import Optional, List


class Window:
    """
    Base class for windows.
    """

    height: int
    width: int
    max_x: int
    max_y: int
    idx: Optional[int]
    opts: Optional[List[str]]

    def __init__(
        self, 
        stdscr, 
        height: int, 
        width: int, 
        idx: Optional[int] = None,
        opts: Optional[List[str]] = None
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

    
    def adjust_yx() -> None:
        pass
