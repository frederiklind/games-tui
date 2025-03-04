import curses
import time
from typing import Optional, List

from games.cards import Card, Rank, Suit
from games.solitaire.solitaire import SolitaireGame
from ui.window import Window


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

    def __init__(self, stdscr, width, height) -> None:
        """
        Initializes a new solitaire UI.

        Args:
            stdscr ("curses.stdscr"): The curses standard screen.
            width (int): The width of the window.
            height (int): The height of the window.
        """
        super().__init__(stdscr, width, height, idx=0, render_win=True)

        self.sy_a = 3
        self.sy_b = 10
        self.sx = [8, 18, 28, 38, 48, 58, 68]  # initialize x offsets

        self.game = SolitaireGame()
        self.r = 0
        self.c = 0
        self.z = 0

        self.render_game()
        self.run()

    def render_game(self) -> None:
        """
        Full game render.
        """
        self.render_stockile()
        self.render_wastepile()
        self.render_foundation_piles()
        self.render_columns()
        self.win.refresh()

    # This might need some work
    def render_stockile(self) -> None:
        is_hover = (self.r, self.c) == (0, 0)
        sx = self.sx[0]
        if not self.game.stockpile.is_empty():
            self.render_frame(
                self.sy_a, 
                sx, card=self.game.stockpile.peek_top(), 
                is_hover=is_hover, 
                is_top=True
            )
        else:
            self.render_frame(self.sy_a, sx, is_hover=is_hover)
            self.win.addstr(self.sy_a + 2, sx + 4, "", curses.color_pair(3))
            self.win.addstr(self.sy_a + 4, sx + 2, "RESET", curses.color_pair(4))

    def render_wastepile(self) -> None:
        is_hover = (self.r, self.c) == (0, 1)
        sx = self.sx[1]
        self.render_frame(self.sy_a, sx, card=self.game.peek_waste_pile(), is_hover=is_hover)

    def render_columns(self) -> None:
        for i in range(len(self.game.columns)):
            self.render_column(i)

    def render_column(self, idx: int, selected: Optional[Card] = None) -> None:
        sy = self.sy_b
        cards = list(self.game.columns[idx])
        if len(cards) == 0:
            selected = self.r == 1 and self.c == idx and self.z == 0
            self.render_frame(sy, self.sx[idx], is_hover=selected)
        else:
            for i in range(len(cards)):
                selected = self.r == 1 and self.c == idx and self.z == i
                self.render_frame(
                    sy, 
                    self.sx[idx], 
                    card=cards[i], 
                    is_top=(i == len(self.game.columns[idx]) - 1),
                    is_hover=selected
                )
                sy += 2 if cards[i].face_up() else 1
                sy += 1 if selected else 0

    def render_preview_column(self, cards: List[Card]) -> None:
        pass

    def render_foundation_piles(self) -> None:
        for i in range(len(self.game.foundation_piles)):
            sx = self.sx[i + 3]
            self.render_frame(self.sy_a, sx, card=self.game.peek_foundation_pile(i))

    def clear_column(self, idx) -> None:
        for i in range(self.game.column_size(idx) + 9):
            self.win.addstr(self.sy_b + i, self.sx[idx], "         ")


    def render_frame(
        self, 
        sy: int, 
        sx: int, 
        is_top: Optional[bool] = True,
        card: Optional[Card] = None, 
        is_hover: Optional[bool] = False,
    ) -> None:
        """ 
         
        """
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
                    "󰡗" if rank == Rank.KING else 
                    "󰡚" if rank == Rank.QUEEN else 
                    str(card.suit())
                )
                self.win.attron(curses.color_pair(color) | curses.A_BOLD)
                self.win.addstr(
                    sy, sx + 2, f"{str(card.rank()).ljust(3)} {str(card.suit())}"
                )
                self.win.addstr(
                    sy + 2, sx + 4, center_piece, curses.color_pair(color)
                )
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
        self.win.addstr(0, 1, f"{self.r} {self.c} {self.z}" )
        self.win.refresh()

    def switch_row(self) -> None:
        """

        """
        if self.r == 0:
            self.r = 1
            clm_size = self.game.column_size(self.c)
            self.z = 0 if clm_size == 0 else clm_size - 1
            self.render_stockile()
            self.render_wastepile()
            if self.game.column_size(self.c) == 1:
                self.clear_column(self.c)
            self.render_column(self.c) 
        else:
            self.z = 0
            if self.c == 0:
                if len(self.game.columns[0]) == 1:
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
        self.win.addstr(0, 1, f"{self.r} {self.c} {self.z}" )
        self.win.refresh()

    def switch_column_card(self, i: int) -> bool:
        """

        """
        card = self.game.column_card_at_index(self.c, self.z - 1)
        if card and card.face_up():
            self.z += i
            self.clear_column(self.c)
            self.render_column(self.c)
            self.win.refresh()
            return True
        return False


    def switch_columns(self, prev: int) -> None:
        """

        """
        clm_size = self.game.column_size(self.c)
        self.z = 0 if clm_size == 0 else clm_size - 1
        self.clear_column(prev)
        self.clear_column(self.c)
        self.render_column(prev)
        self.render_column(self.c)
        self.win.refresh()


    def deal_stockpile(self) -> None:
        pass

    def select_mode(self) -> None:
        if self.game.column_size(self.c) == 0:      # exit function if selected clm empty
            return
        card = self.game.columns[self.c][self.z]
        c = self.c
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx(self.render_game)
            
            if key in [curses.KEY_LEFT, ord("h")]:
                if self.r == 0 and self.c == 1:
                    self.c -= 1
                    self.render_top()
                else:
                    self.c = (self.c - 1) % len(self.game.columns) 
                    prev = 0 if self.c == 6 else self.c + 1
                    self.switch_columns(prev)
            
            elif key in [curses.KEY_RIGHT, ord("l")]:
                if self.r == 0 and self.c == 0:
                    self.c += 1
                    self.render_top()
                else:
                    self.c = (self.c + 1) % len(self.game.columns)
                    prev = 6 if self.c == 0 else self.c - 1
                    self.switch_columns(prev)

            elif key in [curses.KEY_ENTER, 10, 13]:
                if self.c != c:
                    if self.game.push_to_column(card, self.c):
                        self.game.columns[c].pop()
                        if self.game.columns[c]:
                            if not self.game.peek_column(c).face_up():
                                self.game.columns[c][-1].flip()
                        self.clear_column(c)
                        self.render_column(self.c)
                        self.render_column(c)
                        self.win.refresh()
                break
            elif key == 27:
                break

    def run(self) -> None:
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx(self.render_game)
            if key == ord("q"):
                break
            
            if key in [curses.KEY_UP, ord("k")]:
                if self.r == 1:
                    if not self.switch_column_card(-1):
                        self.switch_row()
                else:
                    self.switch_row()

            elif key in [curses.KEY_DOWN, ord("j")]:
                if self.r == 1:
                    if not self.switch_column_card(1):
                        self.switch_row()
                else:
                    self.switch_row()

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
                if self.r == 0 and self.c == 1:
                    if self.game.waste_pile:
                        card = self.game.peek_waste_pile()
                        if self.game.push_to_foundation_pile(card):
                            self.game.waste_pile.pop()
                            self.render_wastepile()
                            self.render_foundation_piles()
                            self.win.refresh()
                if self.r == 1 and self.z + 1 == self.game.column_size(self.c):
                    card = self.game.peek_column(self.c)
                    if self.game.push_to_foundation_pile(card):
                        self.game.columns[self.c].pop()
                        if self.game.columns[self.c]:
                            self.game.columns[self.c][-1].flip()
                            self.z = 0 if self.game.column_size(self.c) == 0 else self.z - 1
                        self.clear_column(self.c)
                        self.render_column(self.c)
                        self.render_foundation_piles()
                        self.win.refresh()


            elif key in [curses.KEY_ENTER, 10, 13]:
                if (self.r, self.c) == (0, 0):
                    if self.game.stockpile.is_empty():
                        self.game.reset_stockpile()
                    else: 
                        self.game.push_to_waste_pile()

                    self.render_stockile()
                    self.render_wastepile()
                    self.win.refresh()
                elif self.r == 1:
                    self.select_mode()
                    

