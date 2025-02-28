import curses
from typing import List, Tuple

from config import size
from games.rubiks.rubiks_ui import RubiksUI
from ui.settings import SettingsUI
from ui.window import Window
from utils import ui_utils


class MainMenu(Window):
    """
    Main menu which shows when the application starts.

    Attributes:
    """

    win: "curses.window"
    banner: List[str]
    menus: List[Tuple[str, str]]
    menu_idx: int

    def __init__(self, stdscr, height: int, width: int) -> None:
        """ """
        super().__init__(
            stdscr,
            height,
            width,
            idx=-1,
            opts=ui_utils.MENU_OPTIONS[0],
        )
        self.menus = ui_utils.MENU_OPTIONS[self.idx]
        self.menu_idx = 0
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
        self.banner = ui_utils.get_banner()
        self.render_banner()
        self.render_opts()

        self.win.refresh()
        self.stdscr.refresh()

    def render_banner(self) -> None:
        """
        Renders the ascii banner in the main window, showing the application name.
        """
        subtitle = "TERMINAL BASED MINI GAMES"
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
        sy = 13
        cx = self.width // 2

        self.win.addstr(sy, cx - 12, f" {" ".join([""] * 22)} ", curses.color_pair(3))
        if self.idx == -1:
            self.win.attron(curses.color_pair(10) | curses.A_BOLD)
        a, b = self.menus[self.menu_idx]
        m = f"{a}  {b}"
        self.win.addstr(sy, cx - len(m) // 2, m,)
        self.win.attroff(curses.color_pair(9) | curses.A_BOLD)
        sy += 3

        for i in range(len(self.opts)):
            icon, opt = self.opts[i]
            if i == self.idx:
                self.win.attron(curses.color_pair(10) | curses.A_BOLD)
                self.win.addstr(sy + i, cx - 6, opt)
                self.win.attroff(curses.color_pair(9) | curses.A_BOLD)
            else:
                self.win.attron(curses.color_pair(9))
                self.win.addstr(sy + i, cx - 6, opt)
                self.win.attroff(curses.color_pair(9))
            self.win.addstr(sy + i, cx - 9, icon, curses.color_pair(11))

    def adjust_maxyx(self) -> None:
        """ """
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.max_y, self.max_x) != (max_y, max_x):
            self.max_y = max_y
            self.max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()
            self.make_win()

    def change_menu(self) -> None:
        """

        """
        self.opts = ui_utils.MENU_OPTIONS[self.menu_idx] 
        self.win.refresh()
         

    def render(self) -> None:
        """ """
        self.render_opts()
        self.win.refresh()

    def run(self) -> None:
        """ """
        self.render()
        # self.__animation_thread.start()

        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx()

            if key in [curses.KEY_UP, ord("k")]:
                if self.idx > -1:  # Prevent going below -1
                    self.idx -= 1

            elif key in [curses.KEY_DOWN, ord("j")]:
                if self.idx < len(self.opts) - 1:
                    self.idx += 1

            if key in [curses.KEY_LEFT, ord("h")]:
                if self.idx == -1:
                    self.menu_idx = (self.menu_idx - 1) % len(self.menus)
                    self.change_menu()

            elif key in [curses.KEY_RIGHT, ord("l")]:
                if self.idx == -1:
                    self.menu_idx = (self.menu_idx + 1) % len(self.menus)
                    self.change_menu()

            elif key in [curses.KEY_ENTER, 10, 13]:
                match self.idx:
                    case 0:
                        RubiksUI(self.stdscr, size.GAME_HEIGHT, size.GAME_WIDHT)
                        self.make_win()
                    case 1:
                        SettingsUI(self.stdscr, size.MAIN_HEIGHT, size.MAIN_WIDTH)
                        self.stdscr.clear()
                        self.stdscr.refresh()
                        self.make_win()
                    case 3:
                        break
            self.render()
