import curses
import random
import threading
import time
from typing import Dict, Optional, Tuple

# from config import settings
from games.rubiks.rubiks import RubiksGame
from ui.window import Window
from utils import ui_utils


class RubiksUI(Window):
    """
    RubiksGame UI contains three main curses windows: Command (moves), cube state, and
    current game info/statistics.

    Attributes:
        game (RubiksGame): The rubiks game instance.
        win_c (curses.window): The center window for displaying the rubiks cube.
        win_l (curses.window): The left window for displaying options.
        win_r (curses.window): The right window for displaying game stats.
    """

    game: RubiksGame
    win_c: "curses.window"
    win_l: "curses.window"
    win_r: "curses.window"
    arw_xys: Dict[int, Tuple[int, int]]
    timer_thread: threading.Thread

    def __init__(self, stdscr, height: int, width: int) -> None:
        """
        Takes the stdscr as argument. Initially clears stdscr,and creates the
        initial windows for the ui elements.

        Args:
            stdscr: The standard screen instance
        """
        super().__init__(stdscr, height, width, 0)

        self.game = RubiksGame()
        self.opts = [
            " TOP    ",
            " BOTTOM ",
            " LEFT   ",
            " RIGHT  ",
            " FRONT  ",
            " BACK   ",
        ]
        self.idx = 0

        self.arw_xys = {
            0: (3, 10),
            1: (11, 10),
            2: (5, 7),
            3: (5, 21),
            4: (5, 14),
            5: (5, 28),
        }
        self.stdscr.clear()
        self.stdscr.refresh()

        self.timer_thread = threading.Thread(target=self.update_timer)
        self.stop_timer_flag = threading.Event()
        self.timer_thread.daemon = True

        self.make_wins()
        time.sleep(0.5)
        # self.shuffle_cube()   # uncomment to actually start legit game.
        self.run()

    def make_wins(self) -> None:
        """
        Creates initial windows in the standard screen.
        """
        # setup windows for ui elements
        sy = self.max_y // 2 - self.height // 2
        sx = self.max_x // 2 - self.width // 2

        self.win_l = curses.newwin(self.height, 18, sy, sx)
        self.win_r = curses.newwin(self.height, 18, sy, sx + 57)
        self.win_l.bkgd(" ", curses.color_pair(7))  # set background color
        self.win_r.bkgd(" ", curses.color_pair(7))

        self.win_l.attron(curses.color_pair(8) | curses.A_BOLD)
        self.win_l.addstr(0, 0, " 󰆦 Moves          ")
        self.win_l.attroff(curses.color_pair(7) | curses.A_BOLD)

        self.win_r.attron(curses.color_pair(8) | curses.A_BOLD)
        self.win_r.addstr(0, 0, " 󰆦 Game           ")
        self.win_r.addstr(6, 0, " 󰔺 Highscore      ")
        self.win_r.attroff(curses.color_pair(7) | curses.A_BOLD)

        self.render_cmds()
        self.render_key_cmd()
        self.render_stats()
        self.render_pr()

        self.win_c = curses.newwin(self.height, 37, sy, sx + 19)

        self.win_c.bkgd(" ", curses.color_pair(7))
        self.render_cube()
        self.render_arw()
        self.win_c.refresh()

        self.win_l.refresh()
        self.win_r.refresh()
        self.stdscr.refresh()

    def make_gameover_win(self, idx: int) -> None:
        height, width = 13, 35
        sy = self.max_y // 2 - self.height // 2
        sx = self.max_x // 2 - self.width // 2
        win = curses.newwin(height, width, sy + 1, sx + 20)
        win.bkgd(" ", curses.color_pair(7))
        win.attron(curses.color_pair(13))
        win.box()
        win.attroff(curses.color_pair(9))

        header = "Congratulations!"
        msg = "You solved the Rubik's cube."
        y, x = win.getmaxyx()
        sy, sx = y // 2, x // 2

        win.addstr(2, (sx - len(header) // 2) - 2, "", curses.color_pair(2))
        win.attron(curses.color_pair(12) | curses.A_BOLD)
        win.addstr(2, (sx - len(header) // 2) + 1, header)
        win.attroff(curses.color_pair(9) | curses.A_BOLD)
        win.addstr(4, sx - len(msg) // 2, msg, curses.color_pair(9))

        opts = [
            "Start Over",
            "Exit to menu",
        ]
        for i in range(len(opts)):
            if i == idx:
                win.attron(curses.color_pair(10) | curses.A_BOLD)
                win.addstr(7 + i, (sx - len(opts[i]) // 2) + 1, opts[i])
                win.attroff(curses.color_pair(9) | curses.A_BOLD)
            else:
                win.addstr(7 + i, (sx - len(opts[i]) // 2) + 1, opts[i])

        win.refresh()
        self.stdscr.refresh()
        return win

    def game_over(self, state: bool) -> bool:
        """ """
        time.sleep(1)
        idx = 0
        self.make_gameover_win(idx)
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx(True)

            if key in [curses.KEY_DOWN, ord("j")]:
                idx = 1 if idx == 0 else 0
                self.make_gameover_win(idx)

            elif key in [curses.KEY_UP, ord("k")]:
                idx = 1 if idx == 0 else 0
                self.make_gameover_win(idx)

            elif key in [curses.KEY_ENTER, 10, 13]:
                return idx == 0

    def update_timer(self) -> None:
        """ """
        while not self.stop_timer_flag.is_set():
            time.sleep(1)
            self.render_stats()
            self.win_r.refresh()

    def increment_mv(self) -> None:
        """ """
        self.win_r.addstr(3, 5, str(self.game.num_moves), curses.color_pair(9))

    def stop_timer(self) -> None:
        """ """
        self.stop_timer_flag.set()
        self.timer_thread.join()

    def adjust_maxyx(
        self, is_over: Optional[bool] = False, idx: Optional[int] = 0
    ) -> None:
        """
        Checks current stdscr max y and x values, if they do not match values
        stored in state, then UI is re-rendered. The re-rendering is only
        triggered by the window resizing, to maintain a centered UI display.
        """
        max_y, max_x = self.stdscr.getmaxyx()
        if (self.max_y, self.max_x) != (max_y, max_x):
            self.max_y = max_y
            self.max_x = max_x
            self.stdscr.clear()
            self.stdscr.refresh()
            self.make_wins()

            if is_over:
                self.make_gameover_win(idx)

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
        if self.idx in [0, 1]:
            a, b = "", ""
        for i in range(6):
            if i in [0, 1]:
                y, x = self.arw_xys[i]
                sa, sb = (a, b) if i == self.idx else (" ", " ")
                self.win_c.addstr(y, x, sa, curses.color_pair(10))
                self.win_c.addstr(y, x + 8, sb, curses.color_pair(10))
            else:
                y, x = self.arw_xys[i]
                sa, sb = (a, b) if i == self.idx else (" ", " ")
                self.win_c.addstr(y, x, sa, curses.color_pair(10))
                self.win_c.addstr(y + 4, x, sb, curses.color_pair(10))
        self.win_c.refresh()

    # =================================================================================
    # --------------------------- Rendering of UI compoenents -------------------------
    # =================================================================================

    def render_cube(self) -> None:
        """
        Handles updating displayed cube state in the curses window.
        """
        cb = self.game.get_cube()
        for s in range(len(cb)):
            y = self.pos_y(s)
            for r in range(len(cb[s])):
                x = self.pos_x(s)
                for c in range(len(cb[s][r])):
                    self.win_c.addstr(
                        y + r, x + c, "", curses.color_pair(cb[s][r][c] + 1)
                    )
                    x += 1
        self.win_c.refresh()

    def render_cmds(self) -> None:
        """ """
        y = 2
        for i in range(len(self.opts)):
            match i:
                case self.idx:
                    self.win_l.attron(curses.color_pair(10) | curses.A_BOLD)
                    self.win_l.addstr(y + i, 2, f"  {self.opts[i]}  ")
                    self.win_l.attroff(curses.color_pair(9) | curses.A_BOLD)
                case _:
                    self.win_l.addstr(
                        y + i, 2, f"   {self.opts[i]}    ", curses.color_pair(9)
                    )
            self.win_l.addstr(y + i, 4, "", curses.color_pair(i + 1))

    def render_key_cmd(self) -> None:
        """ """
        keys = ["UNDO  : Z", "HINT  : ?", "PAUSE : 󱁐", "OPTS  : 󱊷"]
        symbols = ["󰕌", "", "", "󱤳"]
        y = 9
        for i in range(len(keys)):
            self.win_l.addstr(y + i, 2, symbols[i], curses.color_pair(11))
            self.win_l.addstr(y + i, 5, keys[i], curses.color_pair(9))

    def render_stats(self) -> None:
        """ """
        y = 2
        symbols = ["󰔛", "󱃴"]
        for i in range(len(symbols)):
            self.win_r.addstr(y + i, 2, symbols[i], curses.color_pair(11))
        self.win_r.addstr(
            y + 0, 5, ui_utils.format_time(self.game.time()), curses.color_pair(9)
        )
        self.win_r.addstr(y + 1, 5, f"{str(self.game.num_moves)}", curses.color_pair(9))

    def render_pr(self) -> None:
        """ """
        symbols = ["󰔛", "󱃴"]
        ph = ["00:00:00", "000"]
        y = 10
        for i in range(len(symbols)):
            self.win_r.addstr(y + i, 2, symbols[i], curses.color_pair(11))
            self.win_r.addstr(y + i, 5, ph[i], curses.color_pair(9))

    def render(self) -> None:
        """ """
        self.render_cmds()
        self.win_l.refresh()
        self.win_r.refresh()

    # =================================================================================

    def shuffle_cube(self, n: Optional[int] = None) -> None:
        """
        Shuffles the cube into a random state by performing n rotations,

        """
        time.sleep(0.3)
        for i in range(50):
            face = random.randint(0, 5)
            direction = random.randint(0, 1)
            self.game.move(face, direction)
            self.render_cube()
            time.sleep(0.1)

    def reset(self) -> None:
        self.game = RubiksGame()
        self.shuffle_cube()
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.stop_timer_flag = threading.Event()
        self.timer_thread.daemon = True
        self.game.set_time(time.time())
        self.timer_thread.start()

    def run(self) -> None:
        """
        Main loop for the game. handles key strokes, and re-rendering
        of ui components.
        """
        self.render()
        self.timer_thread.start()

        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx()

            if key in [curses.KEY_UP, ord("k")]:
                self.idx = (self.idx - 1) % len(self.opts)
                self.render_arw()

            elif key in [curses.KEY_DOWN, ord("j")]:
                self.idx = (self.idx + 1) % len(self.opts)
                self.render_arw()

            elif key in [curses.KEY_LEFT, ord("h")]:  # counter clockwise rotaion
                is_valid = self.game.move(self.idx, 1)
                self.render_cube()
                self.game.add(self.idx, 1)
                self.increment_mv()
                if is_valid:
                    self.stop_timer()
                    new = self.game_over(True)
                    if new:
                        self.stdscr.clear()
                        self.stdscr.refresh()
                        self.make_wins()
                        self.reset()
                    else:
                        break

            elif key in [curses.KEY_RIGHT, ord("l")]:  # clockwise rotation
                is_valid = self.game.move(self.idx, 0)
                self.render_cube()
                self.game.add(self.idx, 0)
                self.increment_mv()
                if is_valid:
                    self.stop_timer()
                    new = self.game_over(True)
                    if new:
                        self.stdscr.clear()
                        self.stdscr.refresh()
                        self.make_wins()
                        self.reset()
                    else:
                        break

            elif key == ord("u"):
                if self.game.revert_move():
                    self.render_cube()
                    self.increment_mv()

            elif key == ord("q"):
                self.stop_timer()
                break
            self.render()
