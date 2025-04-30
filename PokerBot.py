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
    print(hand)

    hand = list(hand)
    hand.sort()

    print(hand)
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
    if consecutive == 0.3 and flush:
        return 10
    # Straight Flush    - 9 Points
    if consecutive > 0 and flush:
        return 9
    # Four of a Kind    - 8 Points

    # Full House        - 7 Points

    # Flush             - 6 Points

    # Straight          - 5 Point

    # Three of a Kind   - 4 Points

    # Two Pair          - 3 Points

    # Pair              - 2 Points

    # High Card         - 1 Point

def is_consecutive(hand):
    """Checks if hand is consecutive"""
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

def cards_of_a_kind():
    """Returns how many same-type cards there are.
    If there is a 2 pair, it will return 2 + 2 -> 4.
    If there is a full house, it will return 2 + 3.
    A four of a kind will return 10 (Checks for uniqueness
    as to not mistake it as a 2 pair)."""

    pass
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

    print(is_flush([1,2,3,4,60,13]))

if __name__ == '__main__':
    main()