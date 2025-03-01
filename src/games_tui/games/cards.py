import random

from collections import deque
from enum import Enum
from typing import List, Dict, Deque, Optional


class Suit(Enum):
    """
    The four possible suits of a card, and a fifth
    one for the jokers.
    """
    SPADES = "󰣑"
    HEARTS = "󰋑"
    DIAMONDS = "󰣏"
    CLUBS = "󰣎"
    JOKER = "󱑷"


class Rank(Enum):
    """
    The possible ranks of a playing card.
    """
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"
    JOKER = "JOKER"


class Card(object):
    """
    A single playing card.

    Attributes:
        __rank (Rank): The rank of the card.
        __suit (Suit): The suit of the card.
    """
    __rank: Rank
    __suit: Suit

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """
        Initializes a new playing card with value and color
        specified in arguments of the constructor.

        Args:
            value (str): ...
            suit (str): ...
        """
        self.__rank = rank
        self.__suit = suit

    def rank(self) -> str:
        return self.__rank

    def suit(self) -> str:
        return self.__suit


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

        # Generate 52 cards (13 ranks x 4 suits)
        for suit in Suit:
            if suit != Suit.JOKER:  # Skip Joker in suit loop
                for rank in Rank:
                    if rank != Rank.JOKER:  # Skip Joker in rank loop
                        deck.append(Card(rank, suit))

        # Optionally add Jokers to the deck
        for i in range(jokers):
            deck.append(Card(Rank.JOKER, Suit.JOKER))

        return deque(deck)


    def shuffle(self) -> None:
        """
        Shuffles the cards.
        """
        deck_list = list(self.__cards)      # Convert deque to list for shuffling
        random.shuffle(deck_list)           # Shuffle the list
        self.__cards = deque(deck_list)     # Convert the list back to deque


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

    def tolist(self) -> List[Card]:
        """
        Gets the card deck as a list of cards.

        Returns:
            List[Card]: All cards in the deck.
        """
        return list(self.__cards)
    
    def size(self) -> int:
        """
        Gets the number of card currently in the deck.
        """
        return len(self.__cards)
