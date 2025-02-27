import curses

from typing import List, Optional
from ui.window import Window
from ui.game import GameUI
from ui.settings import SettingsUI
from utils import ui_utils
from config import size


class MainMenu(Window):
    """
    Main menu which shows when the application starts.

    Attributes:
    """
    win: "curses.window"
    banner: List[str]
    opts: List[str]
    icons: List[str]

    def __init__(self, stdscr, height: int, width: int) -> None:
        """

        """
        super().__init__(stdscr, height, width, 0)

        self.opts = ui_utils.menu_options("main")
        self.icons = ui_utils.menu_icons("main")

        self.banner = ui_utils.get_banner()
        self.make_win()
        self.run()

    def make_win(self) -> None:
        """
        Creates the main menu window and renders the ascii banner and menu options.
        """
        sy = self.max_y // 2 - self.height // 2 
        sx = self.max_x // 2 - self.width // 2

        self.win = curses.newwin(self.height, self.width, sy, sx)
        self.win.bkgd(" ", curses.color_pair(7))
        self.render_banner()
        self.render_opts()
        
        author = "frederiklind"
        self.win.addstr(self.height - 2, self.width // 2 - len(author) // 2, author, curses.color_pair(7))
        self.win.addstr(self.height - 2, self.width // 2 - len(author) // 2 - 3, "githere", curses.color_pair(11))

        self.win.refresh()
        self.stdscr.refresh()


    def render_banner(self) -> None:
        """
        Renders the ascii banner in the main window, showing the application name. 
        """
        subtitle = "TERMINAL BASED RUBIK'S CUBE PUZZLE"
        sy = 2
        sx = self.width // 2 - len(self.banner[0]) // 2
        subsx = self.width // 2 - len(subtitle) // 2
        for i, ln in enumerate(self.banner):
            self.win.attron(curses.color_pair(12) | curses.A_BOLD)
            self.win.addstr(sy + i, sx, ln)
        
        self.win.attron(curses.color_pair(9) | curses.A_BOLD)
        self.win.addstr(sy + 1 + len(self.banner), subsx, subtitle)
        self.win.attroff(curses.color_pair(9) | curses.A_BOLD)

    def render_opts(self) -> None:
        """
        Renders the menu options based on the selected option index.
        """
        sy = len(self.banner) + 7
        sx = self.width // 2 - len(self.opts[1]) // 2
        for i in range(len(self.opts)):
            opt = self.opts[i]
            if i == self.idx:
                self.win.attron(curses.color_pair(10) | curses.A_BOLD)
                self.win.addstr(sy + i, sx, opt)
                self.win.attroff(curses.color_pair(9) | curses.A_BOLD)
            else:
                self.win.attron(curses.color_pair(9))
                self.win.addstr(sy + i, sx, opt)
                self.win.attroff(curses.color_pair(9))
            self.win.addstr(sy + i, sx - 1, self.icons[i], curses.color_pair(11))

    def adjust_maxyx(self) -> None:
        """

        """
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.max_y, self.max_x) != (max_y, max_x):
            self.max_y = max_y
            self.max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()
            self.make_win()

    def render(self) -> None:
        """

        """
        self.render_opts()
        self.win.refresh()
            
    def run(self) -> None:
        """

        """
        self.render()
        # self.__animation_thread.start()

        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx()

            if key in [curses.KEY_UP, ord('k')]:
                self.idx = (self.idx - 1) % len(self.opts)

            elif key in [curses.KEY_DOWN, ord('j')]:
                self.idx = (self.idx + 1) % len(self.opts)

            elif key in [curses.KEY_ENTER, 10, 13]:
                match self.idx:
                    case 0:
                        GameUI(self.stdscr, size.GAME_HEIGHT, size.GAME_WIDHT)
                        self.make_win()
                    case 4:
                        SettingsUI(self.stdscr, size.MAIN_HEIGHT, size.MAIN_WIDTH)
                        self.make_win()
                    case 5:
                        break
            self.render()
