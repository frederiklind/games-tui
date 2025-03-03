import curses
import time
from typing import Optional, List

from games.cards import Card, Rank, Suit
from games.solitaire.solitaire import SolitaireGame
from ui.window import Window


class SolitaireUI(Window):
    """ """

    win: "curses.window"
    game: SolitaireGame
    sx: List[int]
    sy_a: int
    sy_b: int
    r: int
    c: int
    z: int

    def __init__(self, stdscr, width, height) -> None:
        super().__init__(stdscr, width, height, idx=0, render_win=True)

        self.sy_a = 3
        self.sy_b = 10
        self.sx = [8, 18, 28, 38, 48, 58, 68]

        self.game = SolitaireGame()
        self.r = 0
        self.c = 0
        self.z = 0

        self.render_game()
        self.run()

    def render_game(self) -> None:
        self.render_stockile()
        self.render_wastepile()
        self.render_foundation_piles()
        self.render_columns()

        self.win.refresh()

    def render_stockile(self) -> None:
        is_hover = (self.r, self.c) == (0, 0)
        sx = self.sx[0]
        if not self.game.stockpile.is_empty():
            self.render_frame(self.sy_a, sx, card=self.game.stockpile.peek_top(), is_hover=is_hover)
        else:
            self.render_frame(self.sy_a, sx, is_hover=is_hover)
            self.win.addstr(self.sy_a + 3, sx + 4, "", curses.color_pair(3))

    def render_wastepile(self) -> None:
        is_hover = (self.r, self.c) == (0, 1)
        sx = self.sx[1]
        if self.game.waste_pile:
            self.render_frame(self.sy_a, sx, card=self.game.waste_pile[-1], is_hover=is_hover)
        else:
            self.render_frame(self.sy_a, sx, is_hover=is_hover)

    def render_columns(self) -> None:
        for i in range(len(self.game.columns)):
            self.render_column(i)

    def render_column(self, idx: int, selected: Optional[Card] = None) -> None:
        sy = self.sy_b
        cards = list(self.game.columns[idx])
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

    def render_foundation_piles(self) -> None:
        for i in range(len(self.game.foundation_piles)):
            # is_hover = (self.r, self.c) == (0, i + 2)
            sx = self.sx[i + 3]
            if self.game.foundation_piles[i]:
                self.render_frame(self.sy_a, sx, card=self.game.foundation_piles[i][-1])
            else:
                self.render_frame(self.sy_a, sx)

    def clear_column(self, idx) -> None:
        for i in range(len(self.game.columns[idx]) + 9):
            self.win.addstr(self.sy_b + i, self.sx[idx], "         ")


    def render_frame(
        self, 
        sy: int, 
        sx: int, 
        is_top: Optional[bool] = True,
        card: Optional[Card] = None, 
        is_hover: Optional[bool] = False,
    ) -> None:
        """ """
        c = 10 if is_hover else 14
        sy += 1 if is_hover and self.r == 1 else 0
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

    def render_top(self) -> None:
        self.render_wastepile()
        self.render_stockile()
        self.render_foundation_piles()
        self.win.addstr(0, 1, f"{self.r} {self.c} {self.z}" )
        self.win.refresh()

    def switch_row(self) -> None:
        if self.r == 0:
            self.r = 1
            self.z = len(self.game.columns[self.c]) - 1
            self.render_stockile()
            self.render_wastepile()
            if len(self.game.columns[self.c]) == 1:
                self.clear_column(0)
            self.render_column(self.c) 
        else:
            self.z = 0
            self.r = 0
            if self.c == 0:
                if len(self.game.columns[0]) == 1:
                    self.clear_column(0)
                self.render_column(0)
                self.render_stockile()
            else:
                x = self.c
                self.c = 1
                self.clear_column(x)
                self.render_column(x)
                self.render_wastepile()
        self.win.addstr(0, 1, f"{self.r} {self.c} {self.z}" )
        self.win.refresh()

    def switch_columns(self, prev: int) -> None:
        self.z = len(self.game.columns[self.c]) - 1
        self.clear_column(prev)
        self.clear_column(self.c)
        self.render_column(prev)
        self.render_column(self.c)
        self.win.refresh()


    def deal_stockpile(self) -> None:
        pass

    def select_mode(self) -> None:
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
                            if not self.game.columns[c][-1].face_up():
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
                self.switch_row()

            elif key in [curses.KEY_DOWN, ord("j")]:
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
                        card = self.game.waste_pile[-1]
                        if self.game.push_to_foundation_pile(card):
                            self.game.waste_pile.pop()
                            self.render_wastepile()
                            self.render_foundation_piles()
                            self.win.refresh()
                if self.r == 1 and self.z + 1 == len(self.game.columns[self.c]):
                    card = self.game.columns[self.c][-1]
                    if self.game.push_to_foundation_pile(card):
                        self.game.columns[self.c].pop()
                        if self.game.columns[self.c]:
                            self.game.columns[self.c][-1].flip()
                            self.z -= 1
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
                    

