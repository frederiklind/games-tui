
import curses
import sys
import signal
from config.settings import settings
from ui.main_menu import MainMenu
from config import size


def signal_handler(sig, frame):
    sys.exit(0)


def main(stdscr):
    """
    Main entry point for the application. Sets up color pairs for curses,
    and initializes the main menu loop.

    Args:
        stdscr: curses standard screen.
    """
    try:
        # Set window title
        sys.stdout.write("\33]0;Games-TUI\a")
        sys.stdout.flush()

        # Do curses setup
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        # Get colors:
        settings.set_colors()

        stdscr.refresh()

        MainMenu(stdscr, size.MAIN_HEIGHT, size.MAIN_WIDTH)  # start main loop

    finally:
        stdscr.clear()
        stdscr.refresh()
        curses.curs_set(1)


signal.signal(signal.SIGINT, signal_handler)

# Start!
curses.wrapper(main)

