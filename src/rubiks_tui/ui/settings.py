import curses

from typing import Dict, List
from config.settings import settings
from ui.figlet import Figlet


class SettingsUI(object):
    """
    Settings UI for the application, from where the user can change
    certain configuration settings set in the toml configuration.

    Attributes:
        __height (int): height of the window
        __width (int): width of the window
    """
    __height: int
    __width: int
    __opts: List[str]
    __color_schemes: List[str]
    __ascii_banners: List[str]
    __keys_presets: List[str]
    __icons: List[str]
    __idx: int
    __colorscheme_idx: int
    __ascii_idx: int
    __max_y: int
    __max_x: int
    __win: "curses.window"

    def __init__(self, stdscr) -> None:
        """
        initializes the main loop of the settings screen.
        """
        self.stdscr = stdscr
        self.__height = 25
        self.__width = 85
        
        # get available colorschemes and ascii banners
        self.__color_schemes = settings.get_colorschemes()
        self.__ascii_banners = settings.get_ascii_banners()
        
        # set initial indices
        self.__idx = 0
        self.__colorscheme_idx = self.__color_schemes.index(settings.color_scheme) 
        self.__ascii_idx = self.__ascii_banners.index(settings.ascii_banner)

        self.__opts = [
            "  Color scheme            ",
            "  Ascii banner            ",
            "  Show window background  ",
            "  Show window borders     ",
            "  Keybinding Preset       ",
        ]
        self.__vals = [
            self.__color_schemes[self.__colorscheme_idx],
            self.__ascii_banners[self.__ascii_idx],
            str(settings.show_background),
            str(settings.show_ui_borders),
            "Vim"
        ]

        self.__keys_presets = [
            "Vim      ",
            "Gamer  ",
        ]

        self.__icons = ["", "", "󰹞", "󰹟", ""]  # "", "", "", "", "", "", "", "󰈆"]

        max_y, max_x = self.stdscr.getmaxyx()
        self.__max_y = max_y
        self.__max_x = max_x
        self.make_win()

        self.run()

    def make_win(self) -> None:
        """
        Creates the window for the settings screen and renders the options
        of the settings menu.
        """
        sy = self.__max_y // 2 - self.__height // 2 
        sx = self.__max_x // 2 - self.__width // 2

        self.__win = curses.newwin(self.__height, self.__width, sy, sx)
        self.__win.bkgd(" ", curses.color_pair(7))

        # draw headers
        self.__win.attron(curses.color_pair(8) | curses.A_BOLD)
        self.__win.addstr(0, 0, " ".join([""] * (self.__width + 1)))
        self.__win.addstr(8, 0, " ".join([""] * (self.__width + 1))) 
        self.__win.addstr(0, 1, "  Settings")
        self.__win.addstr(8, 1, "  Preview")

        self.__win.attroff(curses.color_pair(9) | curses.A_BOLD)
        
        self.render_separator()

        # render opts
        self.render_opts()
        self.render_sample_win()

        self.__win.refresh()
        self.stdscr.refresh()
    
    def render_sample_win(self) -> None:
        for i in range(9, self.__height - 2):
            self.__win.addstr(i, 0, " ".join([""] * (self.__width - 1)), curses.color_pair(1))
            banner = Figlet.get_from_file(self.__ascii_banners[self.__ascii_idx])
        sy = 10
        sx = self.__width // 2 - len(banner[0]) // 2
        self.__win.attron(curses.color_pair(12) | curses.A_BOLD)
        for i in range(len(banner)):
            self.__win.addstr(sy + i, sx, banner[i])
        self.__win.attroff(curses.color_pair(8) | curses.A_BOLD)
        
        sy = 17
        sx = 5
        labels = [
            "TOP", 
            "BOTTOM", 
            "LEFT", 
            "RIGHT", 
            "FRONT", 
            "BACK",       
            "Background", 
            "Headers", 
            "Text", 
            "Selection", 
            "Icons", 
            "ASCII Banner"
        ]

        for i in range(len(labels)):
            c = "" if i == 6 else ""
            clr = 13 if i == 7 else i + 1
            self.__win.addstr(sy + i, sx, c, curses.color_pair(clr))
            self.__win.addstr(sy + i, sx + 4, labels[i], curses.color_pair(9))
            if i == 5:
                sy -= 6
                sx = 20
                    
                        





    def render_separator(self) -> None:
        """

        """
        sy = 2
        sx = self.__width // 2

        for i in range(5):
            self.__win.addstr(sy + i, sx, "│", curses.color_pair(9))


    def render_opts(self) -> None:
        """
        Renders the options of the settings menu.
        """
        sy = 2
        sx_a = 5
        sx_b = 5 + self.__width // 2 
        for i in range(5):
            opt = self.__opts[i]
            if i == self.__idx:
                self.__win.attron(curses.color_pair(10) | curses.A_BOLD)
                self.__win.addstr(sy + i, sx_a, opt)
                self.__win.addstr(sy + i, sx_b, f"< {" ".join([""] * 32)}>")
                self.__win.addstr(sy + i, sx_b + 5, self.__vals[i])
                self.__win.attroff(curses.color_pair(9) | curses.A_BOLD)
            else:
                self.__win.attron(curses.color_pair(9))
                self.__win.addstr(sy + i, sx_a, opt)
                self.__win.addstr(sy + i, sx_b, f"  {" ".join([""] * 32)} ")
                self.__win.addstr(sy + i, sx_b + 5, self.__vals[i])
                self.__win.attroff(curses.color_pair(9))
            self.__win.addstr(sy + i, sx_a - 1, self.__icons[i], curses.color_pair(11))

    def adjust_maxyx(self) -> None:
        """

        """
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.__max_y, self.__max_x) != (max_y, max_x):
            self.__max_y = max_y
            self.__max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()
            self.make_win()

    def render(self) -> None:
        """

        """
        self.render_opts()
        # self.render_key_opts()
        self.render_sample_win()
        self.__win.refresh()

    def increment_carrousel_item(self) -> None:
        match self.__idx:
            case 0:
                if self.__colorscheme_idx == len(self.__color_schemes) - 1:
                    self.__colorscheme_idx = 0
                else:
                    self.__colorscheme_idx += 1
                self.__vals[self.__idx] = self.__color_schemes[self.__colorscheme_idx]
                settings.set_colors(self.__color_schemes[self.__colorscheme_idx]) 
            case 1:
                if self.__ascii_idx == len(self.__ascii_banners) - 1:
                    self.__ascii_idx = 0
                else:
                    self.__ascii_idx += 1
                self.__vals[self.__idx] = self.__ascii_banners[self.__ascii_idx]
        self.update_setting()
    
    def decrement_carrousel_item(self) -> None:
        match self.__idx:
            case 0:
                if self.__colorscheme_idx == 0:
                    self.__colorscheme_idx = len(self.__color_schemes) - 1
                else:
                    self.__colorscheme_idx -= 1
                self.__vals[self.__idx] = self.__color_schemes[self.__colorscheme_idx]
                settings.set_colors(self.__color_schemes[self.__colorscheme_idx]) 
            case 1:
                if self.__ascii_idx == 0:
                    self.__ascii_idx = len(self.__ascii_banners) - 1
                else:
                    self.__ascii_idx -= 1
                self.__vals[self.__idx] = self.__ascii_banners[self.__ascii_idx]
        self.update_setting()

    def update_setting(self) -> None:
        match self.__idx:
            case 0:
                settings.update_toml_value(
                    "ui_display", "color_scheme", self.__color_schemes[self.__colorscheme_idx]
                )
            case 2:
                settings.update_toml_value(
                    "ui_display", "show_background", self.__vals[2] == "True"
                )
                settings.load()
                settings.set_colors()


    def run(self) -> None:
        """
        
        """
        self.render()
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx()

            if key in [curses.KEY_UP, ord("k")]:
                self.__idx = (self.__idx - 1) % len(self.__opts)

            elif key in [curses.KEY_DOWN, ord("j")]:
                self.__idx = (self.__idx + 1) % len(self.__opts)

            elif key in [curses.KEY_LEFT, ord("h")]:
                if self.__idx in [0, 1]:
                    self.decrement_carrousel_item()
                elif self.__idx in [2, 3]:
                    val = self.__vals[self.__idx] == "True"
                    self.__vals[self.__idx] = str(not val)
                    self.update_setting()
                
            elif key in [curses.KEY_RIGHT, ord("l")]:  
                if self.__idx in [0, 1]:
                    self.increment_carrousel_item()
                elif self.__idx in [2, 3]:
                    val = self.__vals[self.__idx] == "True"
                    self.__vals[self.__idx] = str(not val)
                    self.update_setting()

                
            elif key == ord("q"):
                break
            self.render()
