import curses

from typing import Dict, List
from config.settings import settings
from ui.window import Window
from utils.config_utils import ConfigUtils
from utils import ui_utils


class SettingsUI(Window):
    """
    Settings UI for the application, from where the user can change
    certain configuration settings set in the toml configuration.

    Attributes:
        height (int): height of the window.
        width (int): width of the window.
        __
    """
    opts: List[str]
    subopts: Dict[int, int]
    color_schemes: List[str]
    ascii_banners: List[str]
    keys_presets: List[str]
    icons: List[str]
    colorscheme_idx: int
    ascii_idx: int
    win: "curses.window"

    def __init__(self, stdscr, height: int, width: int) -> None:
        """
        initializes the main loop of the settings screen.
        """
        super().__init__(stdscr, height, width, idx=0)

        # get available colorschemes and ascii banners
        self.color_schemes = settings.get_colorschemes()
        self.ascii_banners = settings.get_ascii_banners()
        
        # set initial indices
        self.idx = 0
        self.colorscheme_idx = self.color_schemes.index(settings.color_scheme) 
        self.ascii_idx = self.ascii_banners.index(settings.ascii_banner)

        self.opts = [
            "  Color scheme            ",
            "  Ascii banner            ",
            "  Show window background  ",
            "  Show window borders     ",
            "  Keybinding Preset       ",
        ]
        self.__vals = [
            self.color_schemes[self.colorscheme_idx],
            self.ascii_banners[self.ascii_idx],
            str(settings.show_background),
            str(settings.show_ui_borders),
            "Vim"
        ]

        self.keys_presets = [
            "Vim      ",
            "Gamer  ",
        ]

        self.icons = ["", "", "󰹞", "󰹟", ""]  # "", "", "", "", "", "", "", "󰈆"]
        self.make_win()

        self.run()

    def make_win(self) -> None:
        """
        Creates the window for the settings screen and renders the options
        of the settings menu.
        """
        sy = self.max_y // 2 - self.height // 2 
        sx = self.max_x // 2 - self.width // 2

        self.win = curses.newwin(self.height, self.width, sy, sx)
        self.win.bkgd(" ", curses.color_pair(7))

        # draw headers
        self.win.attron(curses.color_pair(8) | curses.A_BOLD)
        self.win.addstr(0, 0, " ".join([""] * (self.width + 1)))
        self.win.addstr(8, 0, " ".join([""] * (self.width + 1))) 
        self.win.addstr(0, 1, "  Settings")
        self.win.addstr(8, 1, "  Preview")

        self.win.attroff(curses.color_pair(9) | curses.A_BOLD)
        
        self.render_separator()

        # render opts
        self.render_opts()
        self.render_sample_win()

        self.win.refresh()
        self.stdscr.refresh()
    
    def render_sample_win(self) -> None:
        """

        """
        for i in range(9, self.height - 2):
            self.win.addstr(i, 0, " ".join([""] * (self.width - 1)), curses.color_pair(1))
            banner = ui_utils.get_banner(self.ascii_banners[self.ascii_idx])
        sy = 10
        sx = self.width // 2 - len(banner[0]) // 2
        self.win.attron(curses.color_pair(12) | curses.A_BOLD)
        for i in range(len(banner)):
            self.win.addstr(sy + i, sx, banner[i])
        self.win.attroff(curses.color_pair(8) | curses.A_BOLD)
        
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
            self.win.addstr(sy + i, sx, c, curses.color_pair(clr))
            self.win.addstr(sy + i, sx + 4, labels[i], curses.color_pair(9))
            if i == 5:
                sy -= 6
                sx = 20
                    
    def render_separator(self) -> None:
        """
        Draws a vertical separator between the settings headers
        and values in the settings window.
        """
        sy = 2
        sx = self.width // 2

        for i in range(5):
            self.win.addstr(sy + i, sx, "│", curses.color_pair(9))


    def render_opts(self) -> None:
        """
        Renders the options of the settings menu.
        """
        sy = 2
        sx_a = 5
        sx_b = 5 + self.width // 2 
        for i in range(5):
            opt = self.opts[i]
            if i == self.idx:
                self.win.attron(curses.color_pair(10) | curses.A_BOLD)
                self.win.addstr(sy + i, sx_a, opt)
                self.win.addstr(sy + i, sx_b, f"< {" ".join([""] * 32)}>")
                self.win.addstr(sy + i, sx_b + 5, self.__vals[i])
                self.win.attroff(curses.color_pair(9) | curses.A_BOLD)
            else:
                self.win.attron(curses.color_pair(9))
                self.win.addstr(sy + i, sx_a, opt)
                self.win.addstr(sy + i, sx_b, f"  {" ".join([""] * 32)} ")
                self.win.addstr(sy + i, sx_b + 5, self.__vals[i])
                self.win.attroff(curses.color_pair(9))
            self.win.addstr(sy + i, sx_a - 1, self.icons[i], curses.color_pair(11))

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
        Renders settigs menu options, and sample preview components.
        """
        self.render_opts()
        self.render_sample_win()
        self.win.refresh()

    def increment_carrousel_item(self) -> None:
        """

        """
        match self.idx:
            case 0:
                if self.colorscheme_idx == len(self.color_schemes) - 1:
                    self.colorscheme_idx = 0
                else:
                    self.colorscheme_idx += 1
                self.__vals[self.idx] = self.color_schemes[self.colorscheme_idx]
                settings.set_colors(self.color_schemes[self.colorscheme_idx]) 
            case 1:
                if self.ascii_idx == len(self.ascii_banners) - 1:
                    self.ascii_idx = 0
                else:
                    self.ascii_idx += 1
                self.__vals[self.idx] = self.ascii_banners[self.ascii_idx]
        self.update_setting()
    
    def decrement_carrousel_item(self) -> None:
        match self.idx:
            case 0:
                if self.colorscheme_idx == 0:
                    self.colorscheme_idx = len(self.color_schemes) - 1
                else:
                    self.colorscheme_idx -= 1
                self.__vals[self.idx] = self.color_schemes[self.colorscheme_idx]
                settings.set_colors(self.color_schemes[self.colorscheme_idx]) 
            case 1:
                if self.ascii_idx == 0:
                    self.ascii_idx = len(self.ascii_banners) - 1
                else:
                    self.ascii_idx -= 1
                self.__vals[self.idx] = self.ascii_banners[self.ascii_idx]
        self.update_setting()

    def update_setting(self) -> None:
        """
        
        """
        section, header = ConfigUtils.get_toml_headers(self.idx)

        match self.idx:
            case 0:
                settings.update_toml_value(
                    "ui_display", "color_scheme", self.color_schemes[self.colorscheme_idx]
                )

            case 2:
                settings.update_toml_value(
                    "ui_display", "show_background", self.__vals[2] == "True"
                )
                settings.load()
                settings.set_colors()
            case 3:
                settings.update_toml_value(
                    "ui_display", "show_ui_borders", self.__vals[3] == "True"
                )
                settings.load()
                settings.set_colors()

    def run(self) -> None:
        """
        Initiates the mail loop of the settings screen, and handles
        triggering the different key inputs. 
        """
        self.render()
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx()

            if key in [curses.KEY_UP, ord("k")]:
                self.idx = (self.idx - 1) % len(self.opts)

            elif key in [curses.KEY_DOWN, ord("j")]:
                self.idx = (self.idx + 1) % len(self.opts)

            elif key in [curses.KEY_LEFT, ord("h")]:
                if self.idx in [0, 1]:
                    self.decrement_carrousel_item()
                elif self.idx in [2, 3]:
                    val = self.__vals[self.idx] == "True"
                    self.__vals[self.idx] = str(not val)
                    self.update_setting()
                
            elif key in [curses.KEY_RIGHT, ord("l")]:  
                if self.idx in [0, 1]:
                    self.increment_carrousel_item()
                elif self.idx in [2, 3]:
                    val = self.__vals[self.idx] == "True"
                    self.__vals[self.idx] = str(not val)
                    self.update_setting()


                
            elif key == ord("q"):
                break
            self.render()
