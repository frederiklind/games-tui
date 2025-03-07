import unittest
import random
import copy

from src.games_tui.games.cards import Deck


class TestDeck(unittest.TestCase):
    """
    Test class for Deck.
    """    
    
    def setUp(self):
        """
        Initialize card decks.
        """
        self.deck = Deck()
        self.joker_deck = Deck(jokers=3)


    def test_init(self):
        """
        Tests deck initial state. 
        """
        self.assertEqual(self.deck.size(), 52, "Deck has 52 cards.")
        self.assertEqual(self.joker_deck.size(), 55, "Deck has 55, cards")
    

    def test_draw_top(self):
        """
        Test draw card from top of deck.
        """
        top = self.deck.draw_from_top()
        self.assertNotIn(top, list(self.deck), "Card correctly removed from top.")


    def test_draw_bottom(self):
        """
        Test draw card from bottom of deck.
        """
        btm = self.deck.draw_from_bottom()
        self.assertNotIn(btm, list(self.deck), "Card correctly removed from bottom.")


    def test_draw_push_multiple(self):
        """
        Test drawing cards from the top and pushing them to the bottom
        to ensure the deck returns to its initial state.
        """
        init = copy.deepcopy(list(self.deck))

        for i in range(self.deck.size()):
            self.deck.push_to_bottom(self.deck.draw_from_top())

        self.assertEqual(init, list(self.deck), "Deck should be restored to initial state.")


    def test_shuffle(self):
        """
        Tests that deck has changed after shuffle.
        """
        init = copy.deepcopy(list(self.deck))
        self.deck.shuffle()

        self.assertNotEqual(init, list(self.deck), "Deck should not equal to its initial state.")


if __name__ == "__main__":
    unittest.main()
