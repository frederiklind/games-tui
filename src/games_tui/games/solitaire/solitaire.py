import stack

from typing import Stack, Deque, List
from games.cards import Suit, Rank, Card, Deck


class SolitaireGame(object):
    """

    """
    stockpile: Deck    
    waste_pile: Stack[Card]
    foundation_piles: List[Stack[Card]]
    columns: List[Deque[Card]]

    def __init__(self) -> None:
        """

        """
        self.stockpile = Deck(shuffle=True)
        self.waste_pile = []
        self.foundation_piles = [[], [], [], []] 
        self.columns = [[] for _ in range(7)]

        for i in range(7):
            for _ in range(1, i + 1):
                self.columns[i].append(self.deck.draw_from_top())
            self.columns[i].top().flip()

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
            self.stockpile.append(card)

    def push_to_foundation_pile(self, card: Card) -> bool:
        x = card.suit().value
        if card.rank() == Rank.ACE:
            self.foundation_piles[x].push(card)



