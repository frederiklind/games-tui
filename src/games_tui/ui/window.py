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

    def __init__(
        self, 
        stdscr, 
        height: int, 
        width: int, 
        idx: Optional[int] = None,
        opts: Optional[List[Any]] = None
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

    
    def adjust_yx() -> None:
        pass
