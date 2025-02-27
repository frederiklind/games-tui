import os
import time

from enum import Enum
from typing import Optional, List
from config.settings import settings



class Icon(Enum):
    # Start Menu icons:
    GIT = ""
    GAME = ""
    START_MENU = ["", "", "󱌦", "","", "󰈆"]
    CUBE_FACE = ""


def menu_options(scr: str) -> List[str]:
    """

    """
    match scr:
        case "main":
            return [
                "   Start Game     ",
                "   Rubik's Manual ", 
                "   Achievements   ",
                "   Highscores     ",
                "   Settings       ",
                "   Quit           ",
            ]

        case "settings":
            return [
                "  Color scheme            ",
                "  Ascii banner            ",
                "  Show window background  ",
                "  Show window borders     ",
                "  Keybinding Preset       ",
            ]
        case "game":
            return [

            ]
        case "":
            return [

            ]


def menu_icons(scr: str) -> List[str]:
    match scr:
        case "main":
            return ["", "", "󱌦", "","", "󰈆"]
        case _:
            return []
            


def get_banner(filename: Optional[str] = None) -> List[str]:
    """
    Get the ascii banner displayed in the main menu screen from .txt file
    by filename, and returns it as a list of strings.

    Args:
        filename (str): Name of the ascii file.
    Returns:
       List[str]: Each line of the file as a single string stored in a list. 
    """
    fn = filename if filename is not None else settings.ascii_banner

    with open(os.path.join(settings.dir(), "ascii", f"{fn}.txt"), "r") as f:
        return [line for line in f]


def format_time(start_time) -> str:
    """
    Formats elapsed time of the current game into HH:MM:SS.

    Returns:
        str: Elapsed game time in format HH:MM:SS.
    """
    elapsed_seconds = int(time.time() - start_time)
    hours = elapsed_seconds // 3600
    minutes = (elapsed_seconds % 3600) // 60
    seconds = elapsed_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
