import unittest

from IPython.core.display_functions import display

from PokerBot import (
    get_random_card, card_id, is_consecutive, evaluate_hand,
    is_flush, cards_of_a_kind, high_card, better_hand, display_deck
)

class TestPokerBot(unittest.TestCase):

    def test_card_id_known_values(self):
        #self.assertEqual(display_deck(),'')

        self.assertEqual(card_id(13), "Ace of Spades")
        self.assertEqual(card_id(15), "Three of Diamonds")
        self.assertEqual(card_id(52), "Ace of Hearts")
        self.assertEqual(card_id(51), "King of Hearts")

    def test_is_consecutive(self):
        self.assertTrue(is_consecutive([1, 2, 3, 4, 5, 6, 7]), 5.3)
        self.assertFalse(is_consecutive([12, 13, 14, 14, 16, 17]), 0)
        self.assertEqual(is_consecutive([14,14,15,16,17,18,18]), 0.2) # Straight

    def test_is_flush_true(self):
        self.assertTrue(is_flush([1, 2, 3, 4, 13]))

    def test_is_flush_false(self):
        self.assertFalse(is_flush([1, 14, 27, 4, 5]))

    def test_cards_of_a_kind_variants(self):
        self.assertEqual(cards_of_a_kind([1, 1, 1, 1, 2, 2, 3])[0], 4)
        self.assertEqual(cards_of_a_kind([34, 56, 20, 1, 12, 11])[0], 0)
        self.assertEqual(cards_of_a_kind([34, 11, 29, 12, 11])[0], 1)
        self.assertEqual(cards_of_a_kind([34, 34, 56, 78, 12, 12])[0], 2)
        self.assertEqual(cards_of_a_kind([34, 12, 5, 56, 12, 3, 12])[0], 3)
        self.assertEqual(cards_of_a_kind([34, 34, 56, 34, 12, 34, 10])[0], 4)
        self.assertEqual(cards_of_a_kind([34, 34, 56, 56, 1, 56, 10])[0], 5)

    def test_evaluate_hand_ranks(self):
        self.assertEqual(evaluate_hand({1, 2, 48, 49, 50, 51, 52})[0], 10)  # Royal flush
        self.assertEqual(evaluate_hand({1, 2, 3, 4, 5, 6, 7})[0], 9)        # Straight flush
        self.assertEqual(evaluate_hand({13, 2, 26, 39, 2, 52, 20})[0], 8)   # Four of a kind
        self.assertEqual(evaluate_hand({13, 2, 26, 30, 2, 52, 15})[0], 7)   # Full house
        self.assertEqual(evaluate_hand({2, 8, 1, 4, 7, 50, 40})[0], 6)      # Flush
        self.assertEqual(evaluate_hand({8, 9, 23, 37, 12, 50, 48})[0], 5.1) # Straight
        self.assertEqual(evaluate_hand({1, 14, 27, 4, 5, 46, 48})[0], 4)    # Three of a kind
        self.assertEqual(evaluate_hand({20, 33, 4, 50, 6, 19, 52})[0], 3)   # Two pair
        self.assertEqual(evaluate_hand({1, 14, 13, 12, 11, 20, 29})[0], 2)  # One pair
        self.assertEqual(evaluate_hand({1, 44, 13, 12, 11, 20, 29})[0], 1)  # High card

    def test_high_card_and_better_hand(self):
        self.assertEqual(high_card({1,2,3,4,5,6,7}, {1,2,3,4,5,19,17}), 1)
        self.assertEqual(high_card({33,1,3,51,5,35,37}, {1,2,3,4,13,19,17}), 2)
        self.assertEqual(high_card({12,13,14,15,16,17,19}, {38,39,40,41,42,43,45}), 0)
        self.assertEqual(better_hand({1,2,48,49,50,51,52}, {1,2,3,4,5,6,7}), 1)


if __name__ == '__main__':
    unittest.main()


    # Tests
    # print(get_random_card(1))
    # print(get_random_card(set(range(2,53))))
    #
    # print(get_random_card(52))
    # print(get_random_card(10))
    #
    # print ("Expected: AoS, 3oD, AoH, KoH")
    # print(card_id(13), ", ", card_id(15), ", ", card_id(52), ", ", card_id(51))
    #
    # print(card_id(get_random_card(1).pop()))
    #
    # print(is_consecutive([1,2,3,4,5]))
    # print(is_consecutive([12,13,14,14,16]))
    #
    # hand = {12,13,11,10,7,20}
    # print(evaluate_hand(hand))

    # print(is_flush([1,2,3,4,60,13]))

    # Cards of a kind
    # print(cards_of_a_kind([1,1,1,1,2,2,3]))
    # print("Expected: No pairs (0)\n", cards_of_a_kind([34,56,78,20, 1,12,11]))
    # print("Expected: 1 Pair (1)\n",cards_of_a_kind([34,11,29,78,12,11]))
    # print("Expected: 2 Pair (2)\n", cards_of_a_kind([34, 34,56,78,12,12]))
    # print("Expected: 2 Pair (2)\n", cards_of_a_kind([34, 34,56,56,12,12,10]))
    # print("Expected: 3 of a kind (3)\n", cards_of_a_kind([34,12,5,56,12,3,12]))
    # print("Expected: 4 of a kind (4)\n", cards_of_a_kind([34, 34,56,34,12,34,10]))
    # print("Expected: Full House (5)\n", cards_of_a_kind([34, 34,56,56,1,56,10]))

    # # Evaluate hand
    # print("Royal Flush - 10\n", evaluate_hand({1,2,48,49,50,51,52}))
    # print("Royal Flush - 10\n", evaluate_hand({50,52,48,49,12,51,2}))
    # print("Straight Flush - 9\n", evaluate_hand({1,2,3,4,5,6,7}))
    # fofak = {13,2,26,39,2,52,20}
    # for card in fofak:
    #     print(card_id(card))
    # print("Four of a kind - 8\n", evaluate_hand(fofak))
    # full = {13,2,26,30,2,52,15}
    # for card in full:
    #     print(card_id(card))
    # print("Full House - 7\n", evaluate_hand(full))
    # print("Flush - 6\n", evaluate_hand({2,8,1,4,7,50,40}))
    # straight = {8,9,23,37,12,50,48}
    # not_straight = {10,11,12,13,14,15,16}
    # for card in straight:
    #     print(card_id(card))
    # print("Straight - 5\n", evaluate_hand(straight))
    # for card in not_straight:
    #     print(card_id(card))
    # print("NOT Straight - 1\n", evaluate_hand(not_straight))
    #
    # print("Three of a Kind - 4\n", evaluate_hand({1,14,27,4,5,46,48}))
    # print("Two Pair - 3\n", evaluate_hand({20,33,4,50,6,19,52}))
    #
    # for card in {1,14,13,12,11,20,29}:
    #     print(card_id(card))
    # print("One Pair - 2\n", evaluate_hand({1,14,13,12,11,20,29}))
    # print("High Card - 1\n", evaluate_hand({1,44,13,12,11,20,29}))
    #
    # # high_card
    # print("Hand 1 wins - 1:", high_card({1,2,3,4,5,6,7}, {1,2,3,4,5,19,17}))
    # for card in {33,1,3,51,5,35,37}:
    #     print(card_id(card))
    # for card in {1,2,3,4,13,19,17}:
    #     print(card_id(card))
    # print("Hand 2 wins - 2:", high_card({33,1,3,51,5,35,37}, {1,2,3,4,13,19,17}))
    # print("Hands draw  - 0:", high_card({12,13,14,15,16,17,19}, {38,39,40,41,42,43,45}))

    # Better Hand
    # rand_deck1 = get_random_card(7)
    # rand_deck2 = get_random_card(7)
    # print("Hand 1: \n")
    # for card in rand_deck1:
    #     print(card_id(card))
    # print("\n-\nHand 2: \n")
    # for card in rand_deck2:
    #     print(card_id(card))
    #
    # print(better_hand(rand_deck1, rand_deck2))
    # display_deck()

    #print(better_hand({35,36,44,20,21,24,31}, {32,36,14,48,50,24,31}))
    #print(is_consecutive({35,36,44,20,21,24,31}))
    # Hand 1:
    #
    # Ten of Clubs
    # Jack of Clubs
    # Six of Hearts
    # Eight of Diamonds
    # Nine of Diamonds
    # Queen of Diamonds
    # Six of Clubs
    #
    # -
    # Hand 2:
    #
    # Seven of Clubs
    # Jack of Clubs
    # Two of Diamonds
    # Ten of Hearts
    # Queen of Hearts
    # Queen of Diamonds
    # Six of Clubs
    # Score:  (2, [5]) ,  (2, [11])
    # 2

    # Poker Round
    # deck = {2,3,10}
    # deck.update({13,52}  # Pocket Rockets
    # print("Round: ", poker_round({13,52},deck,{2,3,10}))

    # Simulate Rounds
    # simulate_rounds({13,52}, set())
