from collections import deque 
from typing import Deque, List, Optional
from games.cards import Suit, Rank, Card, Deck


class SolitaireGame(object):
    """

    """
    __num_moves: int
    __start_time: float
    stockpile: Deck    
    waste_pile: Deque[Card]
    foundation_piles: List[Deque[Card]]
    columns: List[Deque[Card]]

    def __init__(self) -> None:
        """

        """
        self.__num_moves = 0
        self.stockpile = Deck(shuffle=True)
        self.waste_pile = deque()
        self.foundation_piles = [deque() for _ in range(4)] 
        self.columns = [deque() for _ in range(7)]

        for i in range(7):
            for _ in range(i + 1):
                self.columns[i].append(self.stockpile.draw_from_top())
            self.columns[i][-1].flip()

    def push_to_waste_pile(self) -> None:
        """
         
        """
        if not self.stockpile.is_empty():
            card = self.stockpile.draw_from_top()
            card.flip()
            self.waste_pile.append(card)

    def reset_stockpile(self) -> None:
        while self.waste_pile:
            card = self.waste_pile.pop()
            card.flip()
            self.stockpile.push_to_top(card)

    def push_to_foundation_pile(self, card: Card) -> bool:
        """
         
        """
        x = card.suit().value
        if card.rank() == Rank.ACE:
            self.foundation_piles[x - 1].append(card)
            return True
        if not self.foundation_piles[x - 1]:
            return False

        if self.is_next(card, self.foundation_piles[x - 1][-1]):
            self.foundation_piles[x - 1].append(card)
            return True
        return False

    def push_to_column(self, card: Card, clm: int) -> bool:
        r = card.rank()
        if self.columns[clm]:
            card_b = self.columns[clm][-1]
            if card < card_b and not card.compare_color_to(card_b):
                self.columns[clm].append(card)
                return True
            return False
        else:
            if r == Rank.KING:
                self.columns[clm].append(card)
                return True
            return False

    def draw_from_wastepile(self) -> Optional[Card]:
        """
        Draws a card from top of the waste pile. If empty,
        returns None.

        Returns:
            Optional[Card]: The card on top of the wastepile, None if empty.
        """
        if self.waste_pile:
            return self.waste_pile.pop()
        return None

    def is_next(self, card_a: Card, card_b: Card) -> bool:
        if card_b.rank() == Rank.ACE:
            return card_a.rank() == Rank.TWO
        else:
            return card_a.rank().value == card_b.rank().value + 1

    def moves(self) -> int:
        return self.moves()


