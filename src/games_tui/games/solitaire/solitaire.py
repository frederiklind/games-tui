from collections import deque 
from typing import Deque, List, Optional
from games.cards import Suit, Rank, Card, Deck


class SolitaireGame(object):
    """
    Class for maintaning a solitaire game.

    Attributes:
        __num_moves (int): The number of moves performed in the game.
        __start_time (float): ...
        stockpile (Deck): The remainder of cards after dealing columns.
        waste_pile (Deque[Card]): The wastepile of the game.
        foundation_piles (List[Deque[Card]]): ...
        columns (List[Deck[Card]]): ...
    """
    __num_moves: int
    __start_time: float
    stockpile: Deck    
    waste_pile: Deque[Card]
    foundation_piles: List[Deque[Card]]
    columns: List[Deque[Card]]

    def __init__(self) -> None:
        """
        Initializes a new solitaire game.
        """
        self.__num_moves = 0
        self.stockpile = Deck(shuffle=True)                  # start with shuffled deck
        self.waste_pile = deque()                            # initialize empty wastepile
        self.foundation_piles = [deque() for _ in range(4)]  # initialize empty foundation piles
        self.columns = [deque() for _ in range(7)]           # initialize empty columns
        
        # deal cards to columns:

        for i in range(7):                                              
            for _ in range(i + 1):
                self.columns[i].append(self.stockpile.draw_from_top())  
            self.columns[i][-1].flip()                                  # flip top cards

    def push_to_waste_pile(self) -> bool:
        """
        Draws a card from the stockpile and pushes it to the waste pile,
        if the stockpile is not empty.

        Returns:
            bool: True if card was pushed to wastepile, false otherwise.
        """
        if not self.stockpile.is_empty():           # check stockpile
            card = self.stockpile.draw_from_top()   # draw card
            card.flip()                             # card face up
            self.waste_pile.append(card)            # add to wastepile
            return True
        return False                                # stockpile is empty


    def reset_stockpile(self) -> None:
        """
        Puts all cards from the wastepile back into the stockpile.
        """
        while self.waste_pile:                      # while there is cardz
            card = self.waste_pile.pop()            # pop wastepile
            card.flip()                             # do a kickflip!
            self.stockpile.push_to_top(card)        # push to stockpile

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

    def peek_foundation_pile(self, idx) -> Optional[Card]:
        if self.foundation_piles[idx]:
            return self.foundation_piles[idx][-1]
        return None

    def peek_waste_pile(self) -> Optional[Card]:
        if self.waste_pile:
            return self.waste_pile[-1]
        return None

    def peek_column(self, idx: int) -> Optional[Card]:
        if self.columns[idx]:
            return self.columns[idx][-1]
        return None

    def column_card_at_index(self, clm, idx) -> Optional[Card]:
        if idx < self.column_size(clm) - 1:
            return self.columns[clm][idx]
        return None

    def column_peek_range(self, clm, idx) -> Deque[Card]:
        cards = deque()
        for i in range(len(self.columns[clm]) - 1, idx, -1):
            cards.appendleft(self.columns[clm][i])
        return cards
        
    def foundation_pile(self, idx: int) -> Deque[Card]:
        return self.foundation_piles[idx]

    def column_size(self, idx: int) -> int:
        return len(self.columns[idx])

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
        """
        Checks if the rank of card A is sequentially next to card B.

        Args:
            card_a (Card): ...
            card_b (Card): ...
        Returns:
            bool: True if card_a is sequentially next, else false.
        """
        if card_b.rank() == Rank.ACE:
            return card_a.rank() == Rank.TWO
        return card_a.rank().value == card_b.rank().value + 1


    def moves(self) -> int:
        """
        Returns the number of moves performed in the current game.

        Returns:
            int: The number of moves performed.
        """
        return self.moves()


