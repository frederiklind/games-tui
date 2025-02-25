import curses

from ui.figlet import Figlet
from ui.game import GameUI



class MainMenu(object):
    __opts: [str]
    __idx: int
    __max_y: int
    __max_x: int

    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.__opts = [
            "            New Game            ",
            "           Saved Game           ",
            "              Quit              ",
        ]
        self.__idx = 0
        max_y, max_x = self.stdscr.getmaxyx()
        self.__max_y = max_y
        self.__max_x = max_x
        self.title = Figlet.title()
        self.mw = len(self.title[0])
        self.run()

    def print_title(self) -> None:
        sy = self.__max_y // 2 - 8
        sx = self.__max_x // 2 - self.mw // 2
        for i, ln in enumerate(self.title):
            self.stdscr.addstr(sy + i, sx, ln, curses.color_pair(4))
        self.stdscr.refresh()

    def print_menu(self) -> None:
        sy = self.__max_y // 2
        sx = self.__max_x // 2 - self.mw // 2
        menu_win = curses.newwin(len(self.__opts) + 2, self.mw, sy - 1, sx)

        y = 0
        for i in range(len(self.__opts)):
            opt = self.__opts[i]

            if i == self.__idx:
                menu_win.attron(curses.color_pair(4) | curses.A_BOLD)
                menu_win.addstr(y + 1, 0, opt)
                menu_win.attroff(curses.color_pair(2) | curses.A_BOLD)
            else:
                menu_win.attron(curses.color_pair(2))
                menu_win.addstr(y + 1, 0, opt)
                menu_win.attroff(curses.color_pair(2))
            y += 1
        menu_win.refresh()

    def adjust_maxyx(self) -> None:
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.__max_y, self.__max_x) != (max_y, max_x):
            self.__max_y = max_y
            self.__max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()
            self.print_title()
            self.print_menu()
            


    def run(self) -> None:
        self.print_title()
        self.print_menu()
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx()

            if key in [curses.KEY_UP, ord('k')]:
                self.__idx = (self.__idx - 1) % len(self.__opts)

            elif key in [curses.KEY_DOWN, ord('j')]:
                self.__idx = (self.__idx + 1) % len(self.__opts)

            elif key in [curses.KEY_ENTER, 10, 13]:
                match self.__idx:
                    case 0:
                        # self.stdscr.clear()
                        GameUI(self.stdscr)
                        self.stdscr.clear()
                        self.print_title()  # reprint title, when returning to main
                    case 1:
                        break
                    case 2:
                        break
            self.print_menu()
