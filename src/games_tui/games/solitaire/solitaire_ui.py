import curses
import threading
import time

from collections import deque
from typing import Deque, List, Optional, Tuple

from utils import ui_utils
from games.cards import Card, Rank
from games.solitaire.solitaire import SolitaireGame
from ui.window import Window
from audio.player import Player, Sound


class SolitaireUI(Window):
    """
    The user interface for the solitaire game.

    Attributes:
        game (SolitaireGame): The game obviously.
        sx (List[int]): The list of x offsets for each column.
        sy_a (int): The y offset for row 0.
        sy_b (int): The y offset for row 1.
        r (int): The current row index.
        c (int): The current column index.
        z (int): The current card column index.
    """

    game: SolitaireGame
    sx: List[int]
    sy_a: int
    sy_b: int
    r: int
    c: int
    z: int
    timer_thread: threading.Thread
    stop_timer_flag: threading.Event

    def __init__(self, stdscr, width, height) -> None:
        """
        Initializes a new solitaire UI.

        Args:
            stdscr ("curses.stdscr"): The curses standard screen.
            width (int): The width of the window.
            height (int): The height of the window.
        """
        super().__init__(stdscr, width, height, idx=0, render_win=True)

        # initialize ui offsets

        self.sy_a = 3
        self.sy_b = 10

        sx = 8
        self.sx = [x for x in range(sx, sx + 70, 10)]

        self.game = SolitaireGame()

        self.r = 0      # row index
        self.c = 0      # column index
        self.z = -1     # card index

        # setup timer stuff:

        self.timer_thread = threading.Thread(target=self.update_timer)
        self.stop_timer_flag = threading.Event()
        self.timer_thread.daemon = True

        self.render_game()  # render everything
        self.run()          # run main game loop


    # ======================================================================
    # ---------------------------- Timer Stuff -----------------------------
    # ======================================================================


    def update_timer(self) -> None:
        """
        Updates timer and refreshes window.
        """
        while not self.stop_timer_flag.is_set():
            time.sleep(1)
            self.render_timer()
            self.win.noutrefresh()  # avoid interference with main thread
            curses.doupdate()


    def stop_timer(self) -> None:
        """
        Stops the game timer and returns nothing at all.
        """
        self.stop_timer_flag.set()
        self.timer_thread.join()


    # ======================================================================
    # --------------------- Rendering of UI components ---------------------
    # ======================================================================


    def render_game(self) -> None:
        """
        Full game render.
        """
        self.render_stockile()
        self.render_wastepile()
        self.render_foundation_piles()
        self.render_columns()
        self.render_timer()
        self.render_move_count()
        self.win.refresh()


    def render_timer(self) -> None:
        """
        Renders the current game time in the UI window.
        """
        timestr = ui_utils.format_time(self.game.time())

        self.win.addstr(
            1, self.width - (len(timestr) + 10), "󰔛", curses.color_pair(11)
        )
        
        self.win.addstr(
            1, self.width - (len(timestr) + 8), timestr, curses.color_pair(9)
        )


    def render_move_count(self) -> None:
        """
        Renders the number of moves performed in the current game.
        """
        self.win.addstr(
            1, self.sx[0], "󰘹", curses.color_pair(11)
        )
        
        self.win.addstr(
            1, self.sx[0] + 3, f"Moves: {str(self.game.moves())}", curses.color_pair(9)
        )


    # This might need some work
    def render_stockile(self) -> None:
        """
        Renders the stockpile. Renders backside of card if not empty,
        else a frame indicating empty state.
        """
        is_hover = (self.r, self.c) == (0, 0)   # determine whether user hovers stockpile.
        sx = self.sx[0]
        if not self.game.stockpile.is_empty():
            self.render_frame(
                self.sy_a,
                sx,
                card=self.game.stockpile.peek_top(),
                is_hover=is_hover,
                is_top=True,
            )
        else:
            self.render_frame(self.sy_a, sx, is_hover=is_hover)
            self.win.addstr(self.sy_a + 2, sx + 4, "", curses.color_pair(3))
            self.win.addstr(self.sy_a + 4, sx + 2, "RESET", curses.color_pair(4))


    def render_wastepile(self) -> None:
        """
        Renders the waste pile of the game.
        """
        is_hover = (self.r, self.c) == (0, 1)
        sx = self.sx[1]
        self.render_frame(
            self.sy_a, sx, card=self.game.peek_waste_pile(), is_hover=is_hover
        )


    def render_columns(self) -> None:
        """
        Renders all seven columns of row 1.
        """
        for i in range(len(self.game.columns)):
            self.render_column(i)


    def render_column(self, idx: int) -> None:
        """
        Renders a single column of row 1. If column is empty, a single
        empty frame is rendered in hovered state, otherwise the stack of
        cards are rendered based on their face up state.

        Args:
            idx (int): Index of the column to be rendered.
        """
        sy = self.sy_b
        cards = list(self.game.columns[idx])
        if len(cards) == 0:
            selected = self.rcz() == (1, idx, 0)
            self.render_frame(sy, self.sx[idx], is_hover=selected)
        else:
            for i in range(len(cards)):
                selected = self.rcz() == (1, idx, i)
                self.render_frame(
                    sy,
                    self.sx[idx],
                    card=cards[i],
                    is_top=(i == len(self.game.columns[idx]) - 1),
                    is_hover=selected,
                )
                sy += 2 if cards[i].face_up() else 1
                sy += 1 if selected else 0


    def render_preview_column(self, idx: int, selected_cards: List[Card]) -> None:
        """
        Renders a column with preview selection stacked on top 
        of selected column. To be used on selected mode only.

        Args:
            idx (int): Index of the column to be rendered.
            selected_cards (List[Card]): Selected cards to be previewed over column.
        """
        sy = self.sy_b
        cards = list(self.game.columns[idx])
        if len(cards) == 0:
            selected = self.r == 1 and self.c == idx and self.z == 0
            self.render_frame(sy, self.sx[idx], is_hover=selected)
            sy -= 1
        else:
            for i in range(len(cards)):
                self.render_frame(
                    sy,
                    self.sx[idx],
                    card=cards[i],
                    is_top=(i == len(self.game.columns[idx]) - 1),
                    is_hover=False,
                )
                sy += 2 if cards[i].face_up() else 1

        # render the selected cards:

        for i in range(len(selected_cards)):
            selected = i == 0
            is_top = i == len(selected_cards) - 1
            self.render_frame(
                sy,
                self.sx[idx],
                card=selected_cards[i],
                is_top=is_top,
                is_hover=selected,
            )
            sy += 3 if selected else 2


    def render_foundation_piles(self) -> None:
        """
        Renders all four foundation piles. Renders an empty frame if
        a foundation pile is empty, otherwise the card placed on top.
        """
        for i in range(len(self.game.foundation_piles)):
            sx = self.sx[i + 3]
            self.render_frame(self.sy_a, sx, card=self.game.peek_foundation_pile(i))


    def clear_column(self, idx: int) -> None:
        """ 
        Clears column at index of row 1. 
        """
        sy = self.sy_b
        while sy < self.height - 2:
            self.win.addstr(sy, self.sx[idx], " " * 9)
            sy += 1


    def render_frame(
        self,
        sy: int,
        sx: int,
        is_top: Optional[bool] = True,
        card: Optional[Card] = None,
        is_hover: Optional[bool] = False,
    ) -> None:
        """ 
        Renders a card frame. 
        """

        if sy + 4 > self.height - 8:
            return
        c = 10 if is_hover else 14
        sy += 1 if is_hover and card and self.r == 1 else 0
        self.win.attron(curses.color_pair(c))
        self.win.addstr(sy, sx, "╭───────╮")
        self.win.addstr(sy + 1, sx, "│       │")
        self.win.addstr(sy + 2, sx, "│       │")
        sy += 1
        if is_top:
            for i in range(5):
                self.win.addstr(sy + i, sx, "│       │")
            self.win.addstr(sy + 5, sx, "╰───────╯")
        if card:
            if card.face_up():
                color = card.color()
                rank = card.rank()
                center_piece = (
                    "󰡗"
                    if rank == Rank.KING
                    else "󰡚" if rank == Rank.QUEEN else str(card.suit())
                )
                self.win.attron(curses.color_pair(color) | curses.A_BOLD)
                self.win.addstr(
                    sy, sx + 2, f"{str(card.rank()).ljust(3)} {str(card.suit())}"
                )
                self.win.addstr(sy + 2, sx + 4, center_piece, curses.color_pair(color))
                self.win.addstr(
                    sy + 4, sx + 2, f"{str(card.suit())} {str(card.rank()).rjust(3)}"
                )
            else:
                n = 5 if is_top else 1  # prevent unnecessesary pattern print
                for i in range(n):
                    self.win.addstr(sy + i, sx + 1, "▞▚▞▚▞▚▞", curses.color_pair(13))


    def render_top(self) -> None:
        """
        Renders the top row components. Renders waste pile, stockpile
        and all foundation piles.
        """
        self.render_wastepile()
        self.render_stockile()
        self.render_foundation_piles()

        self.win.refresh()


    # ======================================================================
    # ------------------------ UI Navigation Helpers -----------------------
    # ======================================================================


    def switch_row(self, i: int, selection: Optional[Deque[Card]] = None) -> None:
        """
        Switches between rows in the UI window.

        Args:
            i (int): ...
            selection (Optional[Deque[Card]]): (Optional) Selected cards, None by default.
        """
        if self.r == 0:
            if i == -1:
                return
            self.r += i
            clm_size = self.game.column_size(self.c)
            self.z = 0 if clm_size == 0 else clm_size - 1
            self.render_stockile()
            self.render_wastepile()

            if self.game.column_size(self.c) == 1:
                self.clear_column(self.c)
            if selection:
                self.render_preview_column(self.c, selection)
            else:
                self.render_column(self.c)
        else:
            self.z = -1                     # settting this to -1 for proper clm re-render
            self.r += i                     # increment/decrement row index
            if self.c == 0:
                self.clear_column(0)
                self.render_column(0)
                self.render_stockile()
            else:
                self.r == 0
                x = self.c
                self.c = 1
                self.clear_column(x)
                self.render_column(x)
                self.render_wastepile()
        self.win.refresh()


    def switch_column_card(self, i: int) -> bool:
        """
        Handles switching between face-up cards in a column.
0
        Args:
            i (int): Next selection index.
        Returns:
            bool: True if the card at index z + i doesn't exceed column size. False otherwise.
        """
        if self.z == 0 and i == -1:
            return False
        clm_size = self.game.column_size(self.c)
        if clm_size > 1:
            card = self.game.column_card_at_index(self.c, self.z + i)
            if card and card.face_up():
                self.z = self.z + i
                self.clear_column(self.c)
                self.render_column(self.c)
                self.win.refresh()
                return True
        self.win.refresh()
        return False


    def switch_columns(
        self, prev: int, selection: Optional[Deque[Card]] = None
    ) -> None:
        """ """
        clm_size = self.game.column_size(self.c)

        self.z = 0 if clm_size == 0 else clm_size - 1

        self.clear_column(prev)
        self.clear_column(self.c)
        self.render_column(prev)

        if selection:
            self.render_preview_column(self.c, selection)
        else:
            self.render_column(self.c)
        self.win.refresh()


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
    

    def make_gameover_win(self, idx: int) -> None:
        """

        """
        height, width = 13, 45
        sy = self.max_y // 2 - height // 2
        sx = self.max_x // 2 - width // 2
        
        win = curses.newwin(height, width, sy, sx)

        Player.play(Sound.SOLITAIRE_WIN)
        
        win.bkgd(" ", curses.color_pair(7))
        win.attron(curses.color_pair(13))
        win.box()
        win.attroff(curses.color_pair(9))

        header = "Congratulations!"
        msg = "You won the game"
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


    def reset(self) -> None:
        """
        Starts a new game.
        """
        self.r = 0
        self.c = 0
        self.z = -1

        self.game = SolitaireGame()
        self.render_game()

        self.timer_thread = threading.Thread(target=self.update_timer)
        self.stop_timer_flag = threading.Event()
        self.timer_thread.daemon = True
        self.game.set_time(time.time())
        self.timer_thread.start()


    def rcz(self) -> Tuple[int, int, int]:
        """
        Returns rcz of self.
        """
        return (self.r, self.c, self.z)
        

    # ================================================================================
    # ------------------------------ Event handlers ----------------------------------
    # ================================================================================

    """
    functions for handling the differnet key press events.
        
        - Navigation-keys - for navigation between cards and piles. 
        - Escape-key      - for exiting selection-mode.
        - M-key           - for moving a card to the foundation piles.
    """

    def on_key_up(self, i: int):
        """ """
        if self.r == 1:
            if not self.switch_column_card(i):
                self.switch_row(i)
        else:
            self.switch_row(i)


    def on_key_down(self, i: int):
        """ """
        if self.r == 1:
            self.switch_column_card(i)
        else:
            self.switch_row(i)


    def on_key_m(self) -> bool:
        """
        Handles moving a card to the foundation piles.
        """
        # attempt moving a card from waste pile:

        if self.r == 0 and self.c == 1:
            if self.game.waste_pile:
                card = self.game.peek_waste_pile()
                
                if self.game.push_to_foundation_pile(card):
                    Player.play(Sound.CARD_FLIP) 
                    self.game.waste_pile.pop()
                    self.render_wastepile()
                    self.render_foundation_piles()
                    self.render_move_count()
                    self.win.refresh()

                    return self.game.is_solved()
        
        # attempt moving a card from column:

        if self.r == 1 and self.z + 1 == self.game.column_size(self.c):
            card = self.game.peek_column(self.c)
            if self.game.push_to_foundation_pile(card):
                self.game.columns[self.c].pop()
                
                if self.game.column_size(self.c) > 0:
                    Player.play(Sound.CARD_FLIP) 
                    self.game.flip_last(self.c)
                    self.z = 0 if self.game.column_size(self.c) == 0 else self.z - 1
                    
                self.clear_column(self.c)
                self.render_column(self.c)
                self.render_foundation_piles()
                self.render_move_count()
                self.win.refresh()

                return self.game.is_solved()

        return False


    def on_key_enter(self) -> None:
        """ """
        if (self.r, self.c) == (0, 0):
            if self.game.stockpile.is_empty():
                self.game.reset_stockpile()
            else:
                Player.play(Sound.CARD_DEAL)
                self.game.push_to_waste_pile()
            self.render_stockile()
            self.render_wastepile()
            self.render_move_count()
            self.win.refresh()
        else:
            self.select_mode()

    # ======================================================================
    # ------------------------ UI Navigation Helpers -----------------------
    # ======================================================================

    def select_mode(self) -> None:
        """ """
        wp = False
        if self.r == 0 and self.c == 1:
            wp = True
            if not self.game.waste_pile:
                return
            cards = deque()
            cards.append(self.game.draw_from_wastepile())
            self.c = 0
            self.switch_row(1, cards)
        else:
            if self.game.column_size(self.c) == 0:  
                return
            cards = self.game.column_get_range(self.c, self.z)
        c = self.c
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx(self.render_game, render_win=True)

            if key in [curses.KEY_LEFT, ord("h")]:
                if self.r == 0 and self.c == 1:
                    self.c -= 1
                    self.render_top()
                else:
                    self.c = (self.c - 1) % len(self.game.columns)
                    prev = 0 if self.c == 6 else self.c + 1
                    self.switch_columns(prev, cards)

            elif key in [curses.KEY_RIGHT, ord("l")]:
                if self.r == 0 and self.c == 0:
                    self.c += 1
                    self.render_top()
                else:
                    self.c = (self.c + 1) % len(self.game.columns)
                    prev = 6 if self.c == 0 else self.c - 1
                    self.switch_columns(prev, cards)

            elif key in [curses.KEY_ENTER, 10, 13]:
                if self.game.add_to_column(self.c, cards):
                    Player.play(Sound.CARD_PLACE)
                    self.game.flip_last(c)
                    new_size = self.game.column_size(self.c)
                    self.z = new_size - 1 if new_size > 0 else 0
                    self.clear_column(c)
                    self.render_column(self.c)
                    self.render_column(c)
                    self.render_move_count()
                    self.win.refresh()
                else:
                    Player.play(Sound.INVALID_1)
                    if wp:
                        self.game.put_back_waste_pile(cards)
                        self.render_wastepile()
                    else:
                        self.game.put_back_clm(c, cards)
                        self.clear_column(c)
                        self.render_column(c)
                    self.clear_column(self.c)
                    self.render_column(self.c)
                    self.render_move_count()
                    self.win.refresh()
                break
            elif key == 27:
                if wp:
                    self.game.put_back_waste_pile(cards)
                    self.render_wastepile()
                else:
                    self.game.put_back_clm(c, cards)
                    self.clear_column(c)
                    self.render_column(c)
                self.clear_column(self.c)
                self.render_column(self.c)
                self.win.refresh()
                break


    def run(self) -> None:
        """
        Main game loop
        """
        self.timer_thread.start()

        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx(self.render_game, render_win=True)

            if key == ord("q"):
                self.stop_timer()
                break

            if key in [curses.KEY_UP, ord("k")]:
                self.on_key_up(-1)

            elif key in [curses.KEY_DOWN, ord("j")]:
                self.on_key_down(1)

            elif key in [curses.KEY_LEFT, ord("h")]:
                if self.r == 0 and self.c == 1:
                    self.c -= 1
                    self.render_top()
                else:
                    prev = self.c  # Store previous column index
                    if self.c > 0:
                        self.c -= 1
                        self.switch_columns(prev)

            elif key in [curses.KEY_RIGHT, ord("l")]:
                if self.r == 0 and self.c == 0:
                    self.c += 1
                    self.render_top()
                else:
                    prev = self.c  # Store previous column index
                    if self.c < len(self.game.columns) - 1:
                        self.c += 1
                        self.switch_columns(prev)

            elif key == ord("m"):
                res = self.on_key_m()
                if res:
                    self.stop_timer()
                    new = self.game_over(True)
                    if new:
                        self.stdscr.clear()
                        self.stdscr.refresh()
                        self.render_win()
                        self.reset()
                    else:
                        break 

            elif key in [curses.KEY_ENTER, 10, 13]:
                self.on_key_enter()
