import stack

from typing import Stack, List
from games.cards import Suit, Rank, Card, Deck


class SolitaireGame(object):
    """

    """
    stockpile: Deck    
    waste_pile: Stack[Card]
    foundation_piles: List[Stack[Card]]
    columns: List[Stack[Card]]

    def __init__(self) -> None:
        """

        """
        self.deck = Deck(shuffle=True)
        self.waste_pile = []
        self.foundation_piles = [[], [], [], []] 

        for i in range(7):
            for j in range(1, i + 1):
                self.foundation_piles[i].append(self.deck.draw_from_top())


    def push_to_stockpile(self, card: Card) -> None:
        if 

