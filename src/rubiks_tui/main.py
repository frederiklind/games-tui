import curses
import sys

from config.settings import settings
from ui.main_menu import MainMenu
from config import size


def main(stdscr):
    """
    Main entry point for the application. Sets up color pairs for curses,
    and initializes the main menu loop.

    Args:
        stdscr: curses standard screen.
    """
    # check_dir()

    # set window title
    sys.stdout.write("\33]0;Rubiks-TUI\a")
    sys.stdout.flush()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    settings.set_colors()
    stdscr.refresh()

    MainMenu(stdscr, size.MAIN_HEIGHT, size.MAIN_WIDTH)  # start main loop

    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)


# start!
curses.wrapper(main)
