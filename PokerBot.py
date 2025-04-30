import random
from collections import Counter

  # 52  % 13   --> is an Ace
  # 1   % 13 --> is a 2

#  [ 4, 12, 13, 14, 15, 16, 23]

def get_random_card(card_count, excluded=None):
    """ Returns set of random card(s) from remaining deck.
    Input: card_count: Number of cards wished to be returned
            excluded: set of cards to be excluded from deck."""
    deck = set(range(1, 53)) # Deck of 52 cards
    if excluded is not None:
        deck = deck - excluded

    cards = set()   # cards to be returned

    for _ in range(card_count):
        card = random.choice(list(deck))
        cards.add(card)
        deck.remove(card) # Remove card from deck

    return cards

def card_id(card):
    """Turn card integer to card id (string)."""
    value = card % 13
    cards_list = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                  "Jack", "Queen", "King"]
    card_str = cards_list[value]
    if 0 <= card <= 13:
        card_str += " of Spades"
    elif 13 < card <= 26:
        card_str += " of Diamonds"
    elif 26 < card <= 39:
        card_str += " of Clubs"
    else:
        card_str += " of Hearts"

    return card_str

def better_hand(hand1, hand2):
    """Takes in 2 set of hands."""
    e1, value_array1 = evaluate_hand(hand1)
    e2, value_array2  = evaluate_hand(hand2)
    print("Score: ", e1, ", ", e2)

    if e1 == 1: # Both are equal to 1- highest card wins
        return high_card(hand1,hand2)     # hand1 WIN = 1, hand2 WIN = 2, DRAW = 0
    elif e1 > e2:     # HAND 1 WINS
        return 1
    elif e1 < e2:    # HAND 2 WINS
        return 2
    elif e1 == e2:   # HANDS ARE EQUAL -> TIE BREAKER (HIGHEST CARDS)
        return high_card(value_array1, value_array2)

    return 0 # Draw elsewhere


def evaluate_hand(hand):
    hand = list(hand)
    hand.sort()

    hand_mod = [card % 13 for card in hand]
    hand_mod.sort()

    # First, check if list is consecutive:
    # Note that the additional decimal value assigned accounts for
    # higher straights beating out lower straights
    if is_consecutive(hand_mod[2:]):
        consecutive = 0.3
    elif is_consecutive(hand_mod[1:6]):
        consecutive = 0.2
    elif is_consecutive(hand_mod[0:5]):
        consecutive = 0.1
    else:
        consecutive = 0

    flush = is_flush(hand)
    # Royal Flush - 10 points
    if consecutive == 0.3 and flush and (hand[6] % 13 == 0): #highest card is ace
        return 10, []
    # Straight Flush    - 9 Points
    if consecutive > 0:
        if (consecutive == 0.1 and is_flush(hand[0:5])) or (
                consecutive == 0.2 and is_flush(hand[1:6])) or (
                consecutive == 0.3 and is_flush(hand[2:])):
            return 9, hand

    # Straight           - 5 Points
        return (5 + consecutive), [] # Decimal value determines if one hand has a higher straight

    kinds, card_types = cards_of_a_kind(hand) # Determines amount of pairs, sets, etc.
                                              # card_types are used for tiebreakers (ie. a better 2-pair)
    # Four of a Kind    - 8 Points
    if kinds == 4:
        return 8, card_types
    # Full House        - 7 Points
    if kinds == 5:
        return 7, card_types
    # Flush             - 6 Points
    if flush:
        return 6, card_types

    # Three of a Kind   - 4 Points
    if kinds == 3:
        return 4, card_types
    # Two Pair          - 3 Points
    if kinds == 2:
        return 3, card_types
    # Pair              - 2 Points
    if kinds == 1:
        return 2, card_types
    # High Card         - 1 Point
    return 1, [] # Handle in another function for tiebreaker

def is_consecutive(hand):
    """Checks if hand is consecutive"""
    print(hand)
    if 0 in hand[1:4]:
        return False

    return(hand[0] + 1 == hand[1] and
       hand[1] + 1 == hand[2] and
       hand[2] + 1 == hand[3] and
       hand[3] + 1 == hand[4])

def is_flush(hand):
    suits = []
    for card in hand:
        if 0 <= card <= 13:
            suits.append(1)
            continue
        if 13 < card <= 26:
            suits.append(2)
            continue
        if 26 < card <= 39:
            suits.append(3)
            continue
        suits.append(4)

    counts = Counter(suits)
    max_key = max(counts, key=counts.get)
    max_value= counts[max_key]
    if max_value >= 5:
        return True
    return False

def cards_of_a_kind(hand):
    hand = [card % 13 for card in hand]
    unique_hand = set(hand)
    """Returns how many same-type cards there are.
    If there are no pairs, it will return 0.
    If there is a 2 pair, it will return 1.
    Two pairs will return 1 + 1, so 2.
    A three of a kind will return 3.
    A four of  a kind will return 4.
    If there is a full house, it will return 2 + 3, so 5.
    (Checks for uniqueness as to not mistake it as a 2 pair)."""
    counts = Counter(hand)
    kinds = 0
    card_type = []
    for card in unique_hand:
        if counts[card] == 4:  # Four of a kind
            kinds = 4
            card_type.append(card)
        if counts[card] == 3:  # 3 of a Kind OR potential Full House
            card_type.append(card)
            if kinds == 1:
                kinds = 5
                continue
            kinds = 3
            continue
        if counts[card] == 2: # 2 pair
            card_type.append(card)
            if kinds == 3:
                kinds = 5
                break
            kinds += 1
            if kinds == 3: # We have found three 2 pairs. Set kinds back to 2. We will take 2 highest pairs
                kinds = 2
                card_type.append(card)


    return kinds, card_type

def high_card(hand1, hand2):
    """Determine highest card as a tiebreaker."""
    hand1 = [card % 13 for card in hand1]
    while 0 in hand1:   # Ace value
        hand1.remove(0)
        hand1.append(13)
    hand2 = [card % 13 for card in hand2]

    while 0 in hand2:   # Ace value
        hand2.remove(0)
        hand2.append(13)

    hand1.sort()
    hand2.sort()

    while hand1 and hand2:
        c1 = hand1.pop()
        c2 = hand2.pop()
        if c1 > c2: # Hand 1 wins high card
            return 1
        elif c1 < c2: # Hand 2 wins high card
            return 2

    return 0  # Identical hand

def display_deck():
    """Displays each card's corresponding numerical value."""
    print("--- -- - DECK- -- --- \n\nCARD - VALUE\n--\n")
    for card in range(1,53):
        print(card_id(card), " - ", card)


def main():
    pass








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
    rand_deck1 = get_random_card(7)
    rand_deck2 = get_random_card(7)
    print("Hand 1: \n")
    for card in rand_deck1:
        print(card_id(card))
    print("\n-\nHand 2: \n")
    for card in rand_deck2:
        print(card_id(card))

    print(better_hand(rand_deck1, rand_deck2))
    #display_deck()

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



if __name__ == '__main__':
    main()