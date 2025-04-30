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
    e1 = evaluate_hand(hand1)
    e2 = evaluate_hand(hand2)
    if e1 > e2:     # HAND 1 WINS
        return 1
    elif e1 < e2:    # HAND 2 WINS
        return 2
    return 0     # DRAW



def evaluate_hand(hand):
    hand = list(hand)
    hand.sort()
    # First, check if list is consecutive:
    # Note that the additional decimal value assigned accounts for
    # higher straights beating out lower straights
    if is_consecutive(hand[2:]):
        consecutive = 0.3
    elif is_consecutive(hand[1:6]):
        consecutive = 0.2
    elif is_consecutive(hand[0:5]):
        consecutive = 0.1
    else:
        consecutive = 0

    flush = is_flush(hand)

    # Royal Flush - 10 points
    if consecutive == 0.3 and flush and (hand[6] % 13 == 0): #highest card is ace
        return 10
    # Straight Flush    - 9 Points
    if consecutive > 0 and flush:
        return 9
    kinds = cards_of_a_kind(hand) # Determines amount of pairs, sets, etc.
    # Four of a Kind    - 8 Points
    if kinds == 4:
        return 8
    # Full House        - 7 Points
    if kinds == 5:
        return 7
    # Flush             - 6 Points
    if flush:
        return 6
    # Straight          - 5 Point
    print("CONSECUTIVE:", consecutive)
    if consecutive > 0:
        return 5 + consecutive  # Decimal value determines if one hand has a higher straight
    # Three of a Kind   - 4 Points
    if kinds == 3:
        return 4
    # Two Pair          - 3 Points
    if kinds == 2:
        return 3
    # Pair              - 2 Points
    if kinds == 1:
        return 2
    # High Card         - 1 Point
    return 1 # Handle in another function for tiebreaker

def is_consecutive(hand):
    """Checks if hand is consecutive"""
    hand = [card % 13 for card in hand]
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
    for card in unique_hand:
        if counts[card] == 4:  # Four of a kind
            return 4
        if counts[card] == 3:  # 3 of a Kind OR potential Full House
            kinds = 3
            continue
        if counts[card] == 2: # 2 pair
            if kinds == 3:
                kinds = 5
                break
            kinds += 1
            if kinds == 2:
                return kinds


    return kinds


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

    # Evaluate hand
    print("Royal Flush - 10\n", evaluate_hand({1,2,48,49,50,51,52}))
    print("Royal Flush - 10\n", evaluate_hand({50,52,48,49,12,51,2}))
    print("Straight Flush - 9\n", evaluate_hand({1,2,3,4,5,6,7}))
    fofak = {13,2,26,39,2,52,20}
    for card in fofak:
        print(card_id(card))
    print("Four of a kind - 8\n", evaluate_hand(fofak))
    full = {13,2,26,30,2,52,15}
    for card in full:
        print(card_id(card))
    print("Full House - 7\n", evaluate_hand(full))
    print("Flush - 6\n", evaluate_hand({2,8,1,4,7,50,40}))
    straight = {8,9,23,37,12,50,48}
    for card in straight:
        print(card_id(card))
    print("Straight - 5\n", evaluate_hand(straight))





if __name__ == '__main__':
    main()