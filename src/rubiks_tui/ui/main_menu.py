import curses
import random
import threading
import time

from typing import List
from ui.figlet import Figlet
from ui.game import GameUI
from ui.settings import SettingsUI


class MainMenu(object):
    """
    Main menu which shows when the application starts.

    Attributes:
        __opts (List[str]): The list of selectable options from the menu.
        __idx (int): Index of the current selected menu option.
        __max_y (int): The max y value for the screen.
        __max_x (int): The max x value for the screen.
    """

    __height: int
    __width: int
    __opts: List[str]
    __icons: List[str]
    __idx: int
    __max_y: int
    __max_x: int
    __win: "curses.window"
    __animation_thread: threading.Thread

    def __init__(self, stdscr) -> None:
        """

        """
        self.stdscr = stdscr
        self.__height = 25
        self.__width = 85
        self.__opts = [
            "   Start Game     ",
            "   Rubik's Manual ",
            "   Achievements   ",
            "   Highscores     ",
            "   Settings       ",
            "   Quit           ",
        ]
        self.__icons = ["", "", "󱌦", "","","󰈆"]
        self.__idx = 0
        max_y, max_x = self.stdscr.getmaxyx()
        self.__max_y = max_y
        self.__max_x = max_x
        self.title = Figlet.title()
        self.make_win()

        # Initialize the animation thread
        # self.__stop_animation_flag = threading.Event()
        # self.__animation_thread = threading.Thread(target=self.animate_rubiks)
        # self.__animation_thread.daemon = True
        
        self.run()

    def make_win(self) -> None:
        """
        Creates the main menu window and renders the ascii banner and menu options.
        """
        sy = self.__max_y // 2 - self.__height // 2 
        sx = self.__max_x // 2 - self.__width // 2

        self.__win = curses.newwin(self.__height, self.__width, sy, sx)
        self.__win.bkgd(" ", curses.color_pair(7))
        self.render_banner()
        # self.render_rubiks()
        self.render_opts()
        
        author = "frederiklind"
        self.__win.addstr(self.__height - 2, self.__width // 2 - len(author) // 2, author, curses.color_pair(7))
        self.__win.addstr(self.__height - 2, self.__width // 2 - len(author) // 2 - 3, "", curses.color_pair(11))

        self.__win.refresh()
        self.stdscr.refresh()


    def render_banner(self) -> None:
        """
        Renders the ascii banner in the main window, showing the application name. 
        """
        subtitle = "TERMINAL BASED RUBIK'S CUBE PUZZLE"
        sy = 2
        sx = self.__width // 2 - len(self.title[0]) // 2
        subsx = self.__width // 2 - len(subtitle) // 2
        for i, ln in enumerate(self.title):
            self.__win.attron(curses.color_pair(12) | curses.A_BOLD)
            self.__win.addstr(sy + i, sx, ln)
        
        self.__win.attron(curses.color_pair(9) | curses.A_BOLD)
        self.__win.addstr(sy + len(self.title), subsx, subtitle)
        self.__win.attroff(curses.color_pair(9) | curses.A_BOLD)

    def render_opts(self) -> None:
        """
        Renders the menu options based on the selected option index.
        """
        sy = len(self.title) + 6
        sx = self.__width // 2 - len(self.__opts[1]) // 2
        for i in range(len(self.__opts)):
            opt = self.__opts[i]
            if i == self.__idx:
                self.__win.attron(curses.color_pair(10) | curses.A_BOLD)
                self.__win.addstr(sy + i, sx, opt)
                self.__win.attroff(curses.color_pair(9) | curses.A_BOLD)
            else:
                self.__win.attron(curses.color_pair(9))
                self.__win.addstr(sy + i, sx, opt)
                self.__win.attroff(curses.color_pair(9))
            self.__win.addstr(sy + i, sx - 1, self.__icons[i], curses.color_pair(11))

    def render_rubiks(self) -> None:
        """
        Handles updating displayed cube state in the curses window.
        """
        # face = [[random.randint(1, 6) for _ in range(3)] for _ in range(3)]
        face = [
            [2, 3, 4],
            [5, 2, 6],
            [1, 5, 4],
        ]
        y = 3
        for r in range(len(face)):
            x = 5
            for c in range(len(face[r])):
                self.__win.addstr(
                    y + r, x + c, "", curses.color_pair(face[r][c])
                )
                x += 1
        self.__win.refresh()

    # def animate_rubiks(self) -> None:
    #     """
    #     Animation loop to update the Rubik's Cube every second.
    #     """
    #     while not self.__stop_animation_flag.is_set():
    #         self.__win.clear()      # Clear window before rendering the updated cube
    #         self.render_banner()    # Re-render the banner
    #         self.render_rubiks()    # Render the Rubik's Cube with new random colors
    #         self.__win.refresh()    # Refresh the window
    #         time.sleep(1)           # Wait for 1 second before updating again
    #
    # def stop_animation(self) -> None:
    #     """
    #     Stop the animation thread.
    #     """
    #     self.__stop_animation_flag.set()
    #     self.__animation_thread.join() 

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
        self.__win.refresh()
            
    def run(self) -> None:
        """

        """
        self.render()
        # self.__animation_thread.start()

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
                        # self.stop_animation()
                        # self.stdscr.clear()
                        GameUI(self.stdscr)
                        self.make_win()
                    case 4:
                        SettingsUI(self.stdscr)
                        self.make_win()
                    case 5:
                        break
            self.render()
