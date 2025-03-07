import random

from collections import deque
from enum import Enum
from typing import List, Deque, Optional, Iterator


class Suit(Enum):
    """
    The four possible suits of a card, and a fifth
    one for the jokers.
    """
    JOKER = 0
    SPADES = 1
    HEARTS = 2
    CLUBS = 3
    DIAMONDS = 4

    __symbols = {
        0: "󱑷",
        1: "󰣑",
        2: "󰋑",
        3: "󰣎",
        4: "󰣏",
    }

    def __str__(self):
        return self.__symbols[self.value]



class Rank(Enum):
    """
    The possible ranks of a playing card.
    """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    JOKER = 0

    def __str__(self) -> str:
        """
        String representation for ranks.
        """
        if self == Rank.JOKER:
            return "JOKER"
        elif self.value >= 11:      # Face cards and ACE
            return self.name[0]     # "J", "Q", "K", "A"
        return str(self.value)


class Card(object):
    """
    A single playing card.

    Attributes:
        __rank (Rank): The rank of the card.
        __suit (Suit): The suit of the card.
        __face_up (bool): Whether the card faces up.
    """
    __rank: Rank
    __suit: Suit
    __face_up: bool

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """
        Initializes a new playing card with value and color
        specified in arguments of the constructor.

        Args:
            value (Rank): Rank of the card. 
            suit (Suit): Suit of the card.
        """
        self.__rank = rank
        self.__suit = suit
        self.__face_up = False

    def rank(self) -> Rank:
        return self.__rank


    def suit(self) -> Suit:
        return self.__suit


    def flip(self) -> None:
        self.__face_up = not self.__face_up


    def face_up(self) -> bool:
        return self.__face_up


    def compare_color_to(self, other: "Card") -> bool:
        return self.__suit.value % 2 == 0 and other.suit().value % 2 == 0


    def color(self) -> int:
        return 5 if self.__suit.value % 2 == 0 else 4 
    

    def __eq__(self, other: "Card") -> bool:
        return self.__rank == other.__rank and self.__suit == other.__suit


    def __lt__(self, other: "Card") -> bool:
        return self.__rank.value < other.__rank.value


    def __gt__(self, other: "Card") -> bool:
        return self.__rank > other.__rank


class Deck(object):
    """
    Generic interface for deck of playing cards. Supports drawing and push 
    operations from both bottom and top of the deck. 

    Attributes:
        __cards (Deque[Card]): Double-ended queue for storing cards.
    """ 
    __cards: Deque[Card]

    def __init__(
        self, 
        jokers: Optional[int] = 0,
        shuffle: Optional[bool] = False
    ) -> None:
        """
        Initializes in sorted state, unless optional shuffle parameter is set 
        to true in the constructor. By default the card desk initializes without 
        jokers, unless the 'jokers' param is set to true.
        """
        self.__cards = deque(self.generate_deck(jokers))
        if shuffle:
            self.shuffle()
        
    def generate_deck(self, jokers: int) -> Deque[Card]:
        """
        Generates a fresh deck of cards.

        Args:
            jokers (bool): Whether to include jokers in the deck.
        Returns:
            Deque[Card]: The generated deck of cards as double-ended queue.
        """
        deck = []
        for suit in Suit:
            if suit != Suit.JOKER:                      # skip Joker
                for rank in Rank:
                    if rank != Rank.JOKER:              # skip Joker again
                        deck.append(Card(rank, suit))

        for i in range(jokers):
            deck.append(Card(Rank.JOKER, Suit.JOKER))

        return deque(deck)


    def shuffle(self) -> None:
        """
        Shuffles the cards.
        """
        deck_list = list(self.__cards)      # convert deque to list for shuffling
        random.shuffle(deck_list)           # shuffle the list
        self.__cards = deque(deck_list)     # convert the list back to deque


    def draw_from_top(self) -> Optional[Card]:
        """
        Draws a card from top of the deck. If deck is empty, returns nothing.

        Returns:
            Optional[Card]: Card from top of the deck if deck is not empty, else None.
        """
        return self.__cards.pop() if self.__cards else None
    
    def draw_from_bottom(self) -> Optional[Card]:
        """
        Draws a card from the bottom of the deck

        Returns:
            Optional[Card]: The bottom card of the deck, returns None if empty.
        """
        return self.__cards.popleft() if self.__cards else None

    def push_to_top(self, card: Card) -> None:
        """
        Pushes a card to the top of the deck.

        Args:
            card (Card): The card to place on top of the deck.
        """
        self.__cards.append(card)

    def push_to_bottom(self, card: Card) -> None:
        """
        Pushes a card to the bottom om the deck

        Args:
            card (Card): The card to place in the bottom of the deck.
        """
        self.__cards.appendleft(card)

    def is_empty(self) -> bool:
        """
        Checks if the card deck is empty.

        Returns:
            bool: True if the deck is empty. 
        """
        return False if self.__cards else True

    def peek_top(self) -> Card:
        if not self.is_empty():
            return self.__cards[-1]
    
    def size(self) -> int:
        """ 
        Gets the number of card currently in the deck. 
        """
        return len(self.__cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self.__cards)
    

if __name__ == "__main__":
    deck = Deck(shuffle=True)
    print(str(deck.draw_from_top().rank()))
