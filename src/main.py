import curses
import os
import sys

from ui.main_menu import MainMenu


def check_dir() -> None:
    """
    Checks directory for saving game states. If not existing,
    the function creates necessary directory in .local/share.
    """
    dir = os.path.join(os.path.expanduser("~"), ".local", "share", "rubiks-tui")
    if not os.path.exists(dir):
        os.makedirs(dir)


def main(stdscr):
    """
    Main entry point for the application. Sets up color pairs for curses,
    and initializes the main menu loop.

    Args:
        stdscr: curses standard screen.
    """
    check_dir()

    # set window title
    sys.stdout.write("\33]0;Rubiks-TUI\a")
    sys.stdout.flush()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    curses.start_color()
    curses.use_default_colors()

    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_RED, -1)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)

        if curses.can_change_color():


            # curses.init_color(10, 960, 663, 498)
            curses.init_color(10, 949, 573, 0) 
            curses.init_pair(6, 10, -1)
            
            # white
            curses.init_color(21, 968, 968, 968) 
            curses.init_pair(11, 21, 15)
            
            # dark background for windows
            curses.init_color(15, 94, 98, 149)
            curses.init_pair(8, -1, 15)
            
            # headers
            # curses.init_color(16, 211, 227, 309)
            curses.init_color(16, 188, 204, 275)
            curses.init_color(17, 502, 529, 635)
            curses.init_pair(9, 17, 16)

            curses.init_pair(10, 17, 15)
            
            # curses.init_pair(11, curses.COLOR_WHITE, 15)
            # yellow
            curses.init_color(22, 988, 925, 12) 
            curses.init_pair(12, 22, 15)

            # green
            curses.init_color(23, 251, 627, 169)
            curses.init_pair(13, 23, 15)

            # blue
            curses.init_color(24, 118, 400, 961)
            curses.init_pair(14, 24, 15)
            # dim blue
            curses.init_pair(35, curses.COLOR_BLUE, 15)

            # red
            curses.init_color(25, 902, 270, 325)
            curses.init_pair(15, 25, 15)
            
            curses.init_pair(16, 10, 15)
            curses.init_pair(17, curses.COLOR_CYAN, 15)
        else:
            curses.init_pair(2, curses.COLOR_MAGENTA, -1)
            curses.init_pair(7, -1, curses.COLOR_BLACK)
            curses.init_pair(8, curses.COLOR_WHITE, -1)

    MainMenu(stdscr)  # start main loop

    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)


# start!
curses.wrapper(main)
