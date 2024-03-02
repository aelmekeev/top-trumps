import unittest
from top_trumps import *

class TestTopTrumps(unittest.TestCase):
    def test_card_get_stat(self):
        card = Card([1, 2, 3])
        self.assertEqual(card.get_stat(0), 1)
        self.assertEqual(card.get_stat(1), 2)
        self.assertEqual(card.get_stat(2), 3)

    def test_card_get_highest_stat_index(self):
        card1 = Card([1, 2, 3, 4])
        card2 = Card([4, 3, 2, 1])
        card3 = Card([1, 2, 2, 0])
        self.assertEqual(card1.get_highest_stat_index(), 3)
        self.assertEqual(card2.get_highest_stat_index(), 0)
        self.assertIn(card3.get_highest_stat_index(), [1, 2])
        self.assertNotIn(card3.get_highest_stat_index(), [0, 3])

    def test_hand_next(self):
        hand = Hand([Card([1, 2, 3, 4]), Card([5, 6, 7, 8])])
        self.assertEqual(hand.next().stats, Card([1, 2, 3, 4]).stats)
        self.assertEqual(hand.next().stats, Card([5, 6, 7, 8]).stats)
        self.assertRaises(IndexError, hand.next)

    def test_hand_add(self):
        hand = Hand([Card([1, 2, 3, 4]), Card([5, 6, 7, 8])])
        self.assertEqual(len(hand.cards), 2)
        hand.add(Card([9, 10, 11, 12]))
        self.assertEqual(len(hand.cards), 3)

    def test_create_card_from_string(self):
        self.assertEqual(create_card_from_string('card1;1;2;3;4').stats, Card([1, 2, 3, 4]).stats)
        self.assertEqual(create_card_from_string('card2;1;2;3;4;5').stats, Card([1, 2, 3, 4, 5]).stats)

    def test_compare_cards(self):
        card1 = Card([1, 2, 3, 4])
        card2 = Card([4, 3, 2, 4])
        card3 = Card([2, 2, 2, 2])
        self.assertEqual(compare_cards([card1, card2], 0), 1)
        self.assertEqual(compare_cards([card1, card2], 2), 0)
        self.assertEqual(compare_cards([card1, card2, card3], 0), 1)
        self.assertIsNone(compare_cards([card2, card3], 2))
        self.assertIsNone(compare_cards([card1, card2, card3], 3))

    def test_deal_2(self):
        deck = [Card([1, 2, 3, 4]), Card([5, 6, 7, 8]), Card([9, 10, 11, 12]), Card([13, 14, 15, 16])]
        hands = deal(deck, 2)
        self.assertEqual(len(hands), 2)
        self.assertEqual(len(hands[0].cards), 2)
        self.assertEqual(len(hands[1].cards), 2)

    def test_deal_3(self):
        deck = [Card([1, 2, 3, 4]), Card([5, 6, 7, 8]), Card([9, 10, 11, 12]), Card([13, 14, 15, 16]), Card([17, 18, 19, 20]), Card([21, 22, 23, 24])]
        hands = deal(deck, 3)
        self.assertEqual(len(hands), 3)
        self.assertEqual(len(hands[0].cards), 2)
        self.assertEqual(len(hands[1].cards), 2)
        self.assertEqual(len(hands[2].cards), 2)

    def test_deal_uneven(self):
        deck = [Card([1, 2, 3, 4]), Card([5, 6, 7, 8]), Card([9, 10, 11, 12]), Card([13, 14, 15, 16]), Card([17, 18, 19, 20])]
        hands = deal(deck, 2)
        self.assertEqual(len(hands), 2)
        self.assertEqual(len(hands[0].cards), 2)
        self.assertEqual(len(hands[1].cards), 2)

    def test_is_end_of_game(self):
        hand1 = Hand([Card([1, 2, 3, 4]), Card([5, 6, 7, 8])])
        hand2 = Hand([])
        hand3 = Hand([Card([9, 10, 11, 12])])
        self.assertTrue(is_end_of_game([hand1, hand2]))
        self.assertFalse(is_end_of_game([hand1, hand2, hand3]))

    def test_play_game_2(self):
        hand1 = Hand([Card([1, 2, 3, 4]), Card([5, 6, 7, 8])])
        hand2 = Hand([Card([9, 10, 11, 12]), Card([13, 14, 15, 16])])
        # >2 2
        # 1 >3
        # 0 4
        self.assertEqual(play_game([hand1, hand2]), 2)

    def test_play_game_3(self):
        hand1 = Hand([Card([1, 2, 3, 4]), Card([5, 6, 7, 8])])
        hand2 = Hand([Card([9, 10, 11, 12]), Card([13, 14, 15, 16])])
        hand3 = Hand([Card([17, 18, 19, 20]), Card([21, 22, 23, 24])])
        # >2 2 2
        # 1 >1 3
        # 0 0 4
        self.assertEqual(play_game([hand1, hand2, hand3]), 2)

    def test_play_game_endless(self):
        hand1 = Hand([Card([1, 2, 3, 4]), Card([13, 14, 15, 16])])
        hand2 = Hand([Card([9, 10, 11, 12]), Card([5, 6, 7, 8])])
        self.assertEqual(play_game([hand1, hand2], 5), 5)

    def test_play_game_bank(self):
        hand1 = Hand([Card([1, 2, 3, 4]), Card([13, 14, 15, 16]), Card([13, 14, 15, 16])])
        hand2 = Hand([Card([1, 2, 3, 4]), Card([5, 6, 7, 8]), Card([5, 6, 7, 8])])
        self.assertEqual(play_game([hand1, hand2]), 3)

if __name__ == '__main__':
    unittest.main()