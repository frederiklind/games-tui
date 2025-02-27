import curses
import random
import threading
import time
from typing import Dict, Tuple, List

from config import settings
from cube.rubiks import Cube


class Game(object):
    """
    Maintains game state, including the Cube instance of current game,
    number of moves used, and timer.

    Attributes:
        cube (Cube): Cube instance used for the current game.
        num_moves (int): Number of moves used for the current game.
    """

    cube: Cube
    num_moves: int
    history: List[Tuple[int, int]]
    __max_hist_len: int

    def __init__(self) -> None:
        """

        """
        self.num_moves = 0
        self.cube = Cube()

    def increment_move_count(self) -> None:
        """
        Increments the number of moves used for the game.
        """
        self.num_moves += 1


class GameUI(object):
    """
    Game UI contains three main curses windows: Command (moves), cube state, and
    current game info/statistics.

    Attributes:
        __opts (List[str]): List of option names available in the game.
        __idx (int): Index representing the currently selected option.
        __cube (Cube): Instance of Cube representing the Rubik's cube.
        __max_y (int): The maximum y-coordinate (rows) of the curses screen.
        __max_x (int): The maximum x-coordinate (columns) of the curses screen.
        __cb_win (_CursesWindow): The curses window used to display the cube.
        __side_pane_l (_CursesWindow): The curses window for displaying commands.
    """

    game: Game
    __width: int
    __height: int
    __opts: [str]
    __idx: int
    __cube: Cube
    __max_y: int
    __max_x: int
    __cb_win: "curses.window"     
    __side_pane_l: "curses.window"
    __side_pane_r: "curses.window"
    __arw_xys: Dict[int, Tuple[int, int]]
    start_time: float
    timer_thread: threading.Thread

    def __init__(self, stdscr) -> None:
        """
        Takes the stdscr as argument. Initially clears stdscr,and creates the
        initial windows for the ui elements.

        Args:
            stdscr: The standard screen instance
        """
        self.game = Game()
        self.__width = 75
        self.__height = 15
        self.__opts = [
            " TOP    ",
            " BOTTOM ",
            " LEFT   ",
            " RIGHT  ",
            " FRONT  ",
            " BACK   ",
        ]
        self.__idx = 0
        self.__n_mv = 0

        self.__arw_xys = {
            0: (3, 10),
            1: (11, 10),
            2: (5, 7),
            3: (5, 21),
            4: (5, 14),
            5: (5, 28),
        }

        self.stdscr = stdscr
        self.start_time = time.time()  # Record the start time after cube is randomized
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.stop_timer_flag = threading.Event()
        self.timer_thread.daemon = True

        self.stdscr.clear()
        self.stdscr.refresh()

        max_y, max_x = self.stdscr.getmaxyx()
        self.__max_y = max_y
        self.__max_x = max_x

        self.__cube = Cube()
        self.make_wins()
        self.shuffle_cube()
        self.run()

    def make_wins(self) -> None:
        """
        Creates initial windows in the standard screen.
        """
        # setup windows for ui elements
        sy = self.__max_y // 2 - self.__height // 2
        sx = self.__max_x // 2 - self.__width // 2

        self.__side_pane_l = curses.newwin(self.__height, 18, sy, sx)
        self.__side_pane_r = curses.newwin(self.__height, 18, sy, sx + 57)
        self.__side_pane_l.bkgd(" ", curses.color_pair(7))  # set background color
        self.__side_pane_r.bkgd(" ", curses.color_pair(7))

        self.__side_pane_l.attron(curses.color_pair(8) | curses.A_BOLD)
        self.__side_pane_l.addstr(0, 0, " 󰆦 Moves          ")
        self.__side_pane_l.attroff(curses.color_pair(7) | curses.A_BOLD)

        self.__side_pane_r.attron(curses.color_pair(8) | curses.A_BOLD)
        self.__side_pane_r.addstr(0, 0, " 󰆦 Game           ")
        self.__side_pane_r.addstr(6, 0, " 󰔺 Highscore      ")
        self.__side_pane_r.attroff(curses.color_pair(7) | curses.A_BOLD)

        self.render_cmds()
        self.render_key_cmd()
        self.render_stats()
        self.render_pr()

        self.__cb_win = curses.newwin(self.__height, 37, sy, sx + 19)

        self.__cb_win.bkgd(" ", curses.color_pair(7))
        self.render_cube()
        self.render_arw()
        self.__cb_win.refresh()

        self.__side_pane_l.refresh()
        self.__side_pane_r.refresh()
        self.stdscr.refresh()


    def format_time(self) -> str:
        """
        Formats elapsed time of the current game into HH:MM:SS.

        Returns:
            str: Elapsed game time in format HH:MM:SS.
        """
        elapsed_seconds = int(time.time() - self.start_time)
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_timer(self) -> None:
        """

        """
        while not self.stop_timer_flag.is_set():
            time.sleep(1)
            self.render_stats()
            self.__side_pane_r.refresh()

    def increment_mv(self) -> None:
        """

        """
        self.game.increment_move_count()
        self.__side_pane_r.addstr(3, 5, str(self.game.num_moves), curses.color_pair(9))

    def stop_timer(self) -> None:
        """

        """
        self.stop_timer_flag.set()
        self.timer_thread.join()


    def adjust_maxyx(self) -> None:
        """
        Checks current stdscr max y and x values, if they do not match values
        stored in state, then UI is re-rendered. The re-rendering is only
        triggered by the window resizing, to maintain a centered UI display.
        """
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.__max_y, self.__max_x) != (max_y, max_x):
            self.__max_y = max_y
            self.__max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()
            self.make_wins()

    # ==================================================================================
    # ---------------------- Selected cube face indicator arrows -----------------------
    # ==================================================================================

    def pos_y(self, face_idx: int) -> int:
        """
        Helper function for gettings the y_a coordinate for the selected face
        indicator arrows, based on the selected face index.

        Args:
            face_idx (int): The index of the selected cube face.
        Returns:
            int: The y_a coordinate of the selected face indicator arrow.
        """
        match face_idx:
            case 0:
                return 2
            case 1:
                return 10
            case _:
                return 6

    def pos_x(self, face_idx: int) -> int:
        """
        Helper function for gettings the x_a coordinate for the selected face
        indicator arrows, based on the selected face index.

        Args:
            face_idx (int): The index of the selected cube face.
        Returns:
            int: The x_a coordinate of the selected face indicator arrow.
        """
        match face_idx:
            case 2:
                return 5
            case 3:
                return 19
            case 5:
                return 26
            case _:
                return 12

    def render_arw(self) -> None:
        """
        Renders arrows pointing to the selected cube face.
        """
        a, b = "", ""
        if self.__idx in [0, 1]:
            a, b = "", ""
        for i in range(6):
            if i in [0, 1]:
                y, x = self.__arw_xys[i]
                sa, sb = (a, b) if i == self.__idx else (" ", " ")
                self.__cb_win.addstr(y, x, sa, curses.color_pair(10))
                self.__cb_win.addstr(y, x + 8, sb, curses.color_pair(10))
            else:
                y, x = self.__arw_xys[i]
                sa, sb = (a, b) if i == self.__idx else (" ", " ")
                self.__cb_win.addstr(y, x, sa, curses.color_pair(10))
                self.__cb_win.addstr(y + 4, x, sb, curses.color_pair(10))
        self.__cb_win.refresh()
    
    # =================================================================================
    # --------------------------- Rendering of UI compoenents -------------------------
    # =================================================================================

    def render_cube(self) -> None:
        """
        Handles updating displayed cube state in the curses window.
        """
        cb = self.__cube.get()
        for s in range(len(cb)):
            y = self.pos_y(s)
            for r in range(len(cb[s])):
                x = self.pos_x(s)
                for c in range(len(cb[s][r])):
                    self.__cb_win.addstr(
                        y + r, x + c, "", curses.color_pair(cb[s][r][c] + 1)
                    )
                    x += 1
        self.__cb_win.refresh()

    def render_cmds(self) -> None:
        """

        """
        y = 2
        for i in range(len(self.__opts)):
            match i:
                case self.__idx:
                    self.__side_pane_l.attron(curses.color_pair(10) | curses.A_BOLD)
                    self.__side_pane_l.addstr(y + i, 2, f"<  {self.__opts[i]}  >")
                    self.__side_pane_l.attroff(curses.color_pair(9) | curses.A_BOLD)
                case _:
                    self.__side_pane_l.addstr(
                        y + i, 2, f"   {self.__opts[i]}    ", curses.color_pair(9)
                    )
            self.__side_pane_l.addstr(y + i, 4, "", curses.color_pair(i + 1))

    def render_key_cmd(self) -> None:
        """

        """
        keys = ["UNDO  : Z", "REDO  : R", "HINT  : ?", "PAUSE : 󱁐", "OPTS  : 󱊷"]
        symbols = ["󰕌", "󰑎", "", "", "󱤳"]
        y = 9
        for i in range(len(keys)):
            self.__side_pane_l.addstr(y + i, 2, symbols[i], curses.color_pair(11))
            self.__side_pane_l.addstr(y + i, 5, keys[i], curses.color_pair(9))

    def render_stats(self) -> None:
        """

        """
        y = 2
        symbols = ["󰔛", "󱃴"]
        for i in range(len(symbols)):
            self.__side_pane_r.addstr(y + i, 2, symbols[i], curses.color_pair(11))
        self.__side_pane_r.addstr(y + 0, 5, self.format_time(), curses.color_pair(9))
        self.__side_pane_r.addstr(y + 1, 5, str(self.game.num_moves), curses.color_pair(9))



    def render_pr(self) -> None:
        """

        """
        symbols = ["󰔛", "󱃴"]
        ph = ["00:00:00", "000"]
        y = 10
        for i in range(len(symbols)):
            self.__side_pane_r.addstr(y + i, 2, symbols[i], curses.color_pair(11))
            self.__side_pane_r.addstr(y + i, 5, ph[i], curses.color_pair(9))

    def render(self) -> None:
        """

        """
        self.render_cmds()
        self.__side_pane_l.refresh()
        self.__side_pane_r.refresh()

    # =================================================================================

    def shuffle_cube(self) -> None:
        """

        """
        time.sleep(0.3)
        for i in range(100):
            side = random.randint(0, 5)
            direction = random.randint(0, 1)
            self.__cube.rotate(side, direction)
            self.render_cube()
            sleep_time = 0.01 + (i / 100) * 0.12
            time.sleep(sleep_time)

    def reset(self) -> None:
        self.game = Game()

    def run(self) -> None:
        """
        Main loop for the game. handles key strokes, and re-rendering
        of ui components.
        """
        self.render()
        self.start_time = time.time()
        self.timer_thread.start()

        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx()

            if key in [curses.KEY_UP, ord("k")]:
                self.__idx = (self.__idx - 1) % len(self.__opts)
                self.render_arw()

            elif key in [curses.KEY_DOWN, ord("j")]:
                self.__idx = (self.__idx + 1) % len(self.__opts)
                self.render_arw()

            elif key in [curses.KEY_LEFT, ord("h")]:  # counter clockwise rotaion
                self.__cube.rotate(self.__idx, 1)
                self.render_cube()
                self.increment_mv()

            elif key in [curses.KEY_RIGHT, ord("l")]:  # clockwise rotation
                self.__cube.rotate(self.__idx, 0)
                self.render_cube()
                self.increment_mv()

            elif key == ord("q"):
                self.stop_timer()
                break
            self.render()
