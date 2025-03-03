from collections import deque 
from typing import Deque, List
from games.cards import Suit, Rank, Card, Deck


class SolitaireGame(object):
    """

    """
    stockpile: Deck    
    waste_pile: Deque[Card]
    foundation_piles: List[Deque[Card]]
    columns: List[Deque[Card]]

    def __init__(self) -> None:
        """

        """
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
            self.stockpile.append(card)

    def push_to_foundation_pile(self, card: Card) -> bool:
        """
         
        """
        x = card.suit().value
        if card.rank() == Rank.ACE:
            self.foundation_piles[x].push(card)
            return True
        
        if self.is_next(card, self.foundation_piles[x][-1]):
            self.foundation_piles[x].append(card)
            return True
        return False


    def is_next(self, card_a: Card, card_b: Card) -> bool:
        if card_b.rank() == Rank.ACE:
            return card_a.rank() == Rank.TWO
        else:
            return card_a.rank().value == card_b.rank().value + 1


