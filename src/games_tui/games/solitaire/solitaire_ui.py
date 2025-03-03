import curses
import time
from typing import Optional

from games.cards import Card, Rank, Suit
from games.solitaire.solitaire import SolitaireGame
from ui.window import Window


class SolitaireUI(Window):
    """ """

    win: "curses.window"
    game: SolitaireGame
    r: int
    c: int

    def __init__(self, stdscr, width, height) -> None:
        super().__init__(stdscr, width, height, idx=0, render_win=True)

        self.game = SolitaireGame()
        self.r = 0
        self.c = 0
        self.z = 0

        self.render_frames()
        self.render_game()
        self.run()

    def render_frames(self) -> None:
        self.render_frame(1, 2)
        self.render_frame(1, 12)
        self.render_frame(1, 32)
        self.render_frame(1, 42)
        self.render_frame(1, 52)
        self.render_frame(1, 62)

        self.render_frame(8, 2)
        self.render_frame(8, 12)
        self.render_frame(8, 22)
        self.render_frame(8, 32)
        self.render_frame(8, 42)
        self.render_frame(8, 52)
        self.render_frame(8, 62)

    def render_game(self) -> None:
        self.render_stockile()
        self.render_wastepile()
        self.render_foundation_piles()
        self.render_columns()

        self.win.refresh()

    def render_stockile(self) -> None:
        is_selected = (self.r, self.c) == (0, 0)
        if not self.game.stockpile.is_empty():
            self.render_frame(1, 2, self.game.stockpile.peek_top(), is_selected=is_selected)
        else:
            self.render_frame(1, 2, is_selected=is_selected)
            self.win.addstr(3, 3, "REDEAL", curses.color_pair(3))

    def render_wastepile(self) -> None:
        is_selected = (self.r, self.c) == (0, 1)
        if self.game.waste_pile:
            self.render_frame(1, 12, self.game.waste_pile[-1], is_selected=is_selected)
        else:
            self.render_frame(1, 12, is_selected=is_selected)

    def render_columns(self) -> None:
        sx = 2
        for i in range(len(self.game.columns)):
            self.render_column(sx, i)
            sx += 10

    def render_column(self, sx: int, idx: int) -> None:
        sy = 8
        cards = list(self.game.columns[idx])
        for i in range(len(cards)):
            self.render_frame(sy, sx, cards[i])
            sy += 2 if cards[i].face_up() else 1

        # self.render_frame(8, 2, Card(Rank.KING, Suit.HEARTS))
        # self.render_frame(8, 12, Card(Rank.TEN, Suit.DIAMONDS))
        # self.render_frame(9, 12, Card(Rank.QUEEN, Suit.CLUBS))
        # self.render_frame(10, 12, Card(Rank.QUEEN, Suit.CLUBS))
        # self.render_frame(11, 12, Card(Rank.QUEEN, Suit.CLUBS))
        # self.render_frame(12, 12, Card(Rank.QUEEN, Suit.CLUBS))
        # self.render_frame(14, 12, Card(Rank.ACE, Suit.SPADES))

    def render_foundation_piles(self) -> None:
        sy, sx = 1, 32
        for i in range(len(self.game.foundation_piles)):
            is_selected = (self.r, self.c) == (0, i + 1)
            if self.game.foundation_piles[i]:
                self.render_frame(sy, sx, self.game.foundation_piles[i][-1], is_selected=is_selected)
            else:
                self.render_frame(sy, sx, is_selected=is_selected)
            sx += 10

    def render_frame(
        self, 
        sy: int, 
        sx: int, 
        card: Optional[Card] = None, 
        is_selected: Optional[bool] = False
    ) -> None:
        """ """
        c = 11 if is_selected else 13
        self.win.attron(curses.color_pair(c))
        self.win.addstr(sy, sx, "╭───────╮")
        sy += 1
        for i in range(5):
            self.win.addstr(sy + i, sx, "│       │")
        self.win.addstr(sy + 5, sx, "╰───────╯")
        if card:
            if card.face_up():
                color = card.color()
                self.win.attron(curses.color_pair(color) | curses.A_BOLD)
                self.win.addstr(
                    sy, sx + 2, f"{str(card.rank()).ljust(3)} {str(card.suit())}"
                )
                self.win.addstr(
                    sy + 2, sx + 4, str(card.suit()), curses.color_pair(color)
                )
                self.win.addstr(
                    sy + 4, sx + 2, f"{str(card.suit())} {str(card.rank()).rjust(3)}"
                )
            else:
                for i in range(5):
                    self.win.addstr(sy + i, sx + 1, "▞▚▞▚▞▚▞", curses.color_pair(13))

        self.win.refresh()

    def render_top(self) -> None:
        self.render_wastepile()
        self.render_stockile()
        self.render_foundation_piles()


    def run(self) -> None:
        while True:
            key = self.stdscr.getch()
            self.adjust_maxyx(self.render_game)
            if key == ord("q"):
                break
            
            if key in [curses.KEY_UP, ord("k")]:
                if self.idx > -1:  # Prevent going below -1
                    self.idx -= 1

            elif key in [curses.KEY_DOWN, ord("j")]:
                if self.idx < len(self.opts) - 1:
                    self.idx += 1

            if key in [curses.KEY_LEFT, ord("h")]:
                self.c -= 2 if self.r == 0 and self.c == 3 else 1
                self.render_top()

            elif key in [curses.KEY_RIGHT, ord("l")]:
                self.c += 2 if self.r == 0 and self.c == 1 else 1
                self.render_top()

            elif key in [curses.KEY_ENTER, 10, 13]:
                if (self.r, self.c) == (0, 0):
                    self.game.push_to_waste_pile()
                    self.render_stockile()
                    self.render_wastepile()
