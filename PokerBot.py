import random
from collections import Counter
import time

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

    if e1 == 1 and e2 == 1: # Both are equal to 1- highest card wins
        return high_card(hand1,hand2)     # hand1 WIN = 1, hand2 WIN = 2, DRAW = 0
    elif e1 > e2:     # HAND 1 WINS
        return 1
    elif e1 < e2:    # HAND 2 WINS
        return 2
    elif e1 == e2:   # HANDS ARE EQUAL -> TIE BREAKER (HIGHEST CARDS)
        return high_card(value_array1, value_array2)

    return 1 # Draw elsewhere - count as a win, since you split the pot


def simulate_rounds(hand, community_cards):

    wins = 0 # Draws will also count as a win - you get your money back, plus some typically, so folding would
             # be a bad play
    plays = 0
    start_time = time.time()
    while time.time() - start_time < 10:
        cards_in_play = set(hand).union(community_cards)

        wins += (poker_round(hand, cards_in_play, community_cards)[0] % 2) # mod 2 for a loss (poker_round returns 2 for opponent win)
        plays += 1
    print("Time: ", time.time() - start_time)
    print("Wins: ", wins)
    print("Plays: ", plays)
    print(f"Win Percentage: {wins / plays*100:.2f}%")
    return wins / plays

def poker_round(hand1, cards_in_play, community_cards):
    # Simulate random opponent hand
    opp_hand = set(get_random_card(2, excluded=cards_in_play))
    if len(community_cards) < 5:
        exclusions = set(hand1).union(community_cards, opp_hand)
        community_cards = set(community_cards).union(get_random_card(5 - len(community_cards), excluded=exclusions)) # Add remaining community cards

    # Add community cards to each player's hand
    full_hand1 = set(hand1).union(community_cards)
    full_opp_hand = set(opp_hand).union(community_cards)

    return better_hand(full_hand1, full_opp_hand), opp_hand






def evaluate_hand(hand):
    hand = list(hand)
    hand.sort()
    hand_mod = []
    for card in hand:
        mod = card % 13
        if mod == 0:
            mod = 13
        if mod not in hand_mod:
            hand_mod.append(mod)
    hand_mod.sort()

    # First, check if list is consecutive:
    # Note that the additional decimal value assigned accounts for
    # higher straights beating out lower straights

    consecutive = is_consecutive(hand_mod)

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
    return 1, card_types # Handle in another function for high card

def is_consecutive(hand):
    """Checks if hand is consecutive"""
    consecutive = 0
    points = 0

    for c in range(len(hand) - 1):
        if hand[c] + 1 == hand[c+1]:
            consecutive += 1
            if consecutive >= 4:
                points = float(c) / 10 - 0.2
        elif hand[c] == hand[c+1]:
            continue
        else:
            consecutive = 0
    return points
    #
    # if 0 in hand[1:4]:
    #     return False
    #
    # return (hand[0] + 1 == hand[1] and
    #    hand[1] + 1 == hand[2] and
    #    hand[2] + 1 == hand[3] and
    #    hand[3] + 1 == hand[4])

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
    hand = [card % 13 if card % 13 != 0 else 13 for card in hand]
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
            break
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

    card_type.sort(key=lambda x: (-counts[x], -x))
    full_hand = []
    for card in counts:
        full_hand += [card] * counts[card]

    # sort by quantity first, then value
    full_hand.sort(key=lambda x: (-counts[x], -x))


    return kinds, full_hand[:5]

def high_card(hand1, hand2):
    """Determine highest card as a tiebreaker. * * ASSUMES SORTED PROPERLY * *"""
    hand1 = [card % 13 if card % 13 != 0 else 13 for card in hand1]
    hand2 = [card % 13 if card % 13 != 0 else 13 for card in hand2]

    while hand1 and hand2:
        c1 = hand1.pop(0)
        c2 = hand2.pop(0)
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

def card_vis_help(card, style="Full"):
    """Displays the card as a typed image."""
    if isinstance(card,int):
        card = card_id(card)
    number = card.split()[0]
    suit = card.split()[2]

    cards_list = {"Ace" : 'A', "Two" : '2', "Three" : '3', "Four" : '4', "Five" : '5', "Six" : '6', "Seven" : '7',
                  "Eight" : '8', "Nine" : '9', "Ten" : '10', "Jack" : 'J', "Queen" : 'Q', "King" : 'K',}

    suits = {"Diamonds" : "\u2666", "Spades" : "\u2660", "Hearts" : "\u2665", "Clubs" : "\u2663"}
    if style == "Full":
        return (" |" + suits[suit] + cards_list[number] + "| " + "\n"
        " |" + cards_list[number] + suits[suit] + "| ")
    elif style == "Half":
        return " |" + suits[suit] + cards_list[number] + "| "
    elif style == "Reverse":
        return " |" + cards_list[number] + suits[suit] + "| "

def card_visual(cards):
    if len(cards) == 1:
        card_vis_help(cards[0], style="Full")
    elif len(cards) > 1:
        vis_cards = ""
        for idx in range(len(cards)):
            vis_cards += card_vis_help(card_id(cards[idx]), style="Half")
        vis_cards += "\n"
        for idx in range(len(cards)):
            vis_cards += card_vis_help(card_id(cards[idx]), style="Reverse")
        print(vis_cards)
    else:
        print("No cards.\n")

def main():
    print("Welcome to PokerBot Probability Simulation!")
    choice = input("Press 'Enter' to begin random simulation,"
                   " or customize hand & community cards (press any"
                   " other key, then 'Enter'). ")
    # Random simulation
    if choice == '':
        round_name = "Pre-Flop"
        com_cards = []
        cards = list(get_random_card(2))
        cards_set = set(cards)

    # Custom simulation
    else:
        while 1:
            hand = input("\nInput two numbers between 1 and 52 to select specific cards (Ex. '13 52').\n"
                         "For a list of the cards to their corresponding integer representation,"
                         " enter 'l'. \nTo randomize your hand, enter 'random'.")
            if hand == 'l':
                display_deck()
            elif hand.lower() == 'random':
                cards = list(get_random_card(2))
                print(f"Your hand:\n card_id(cards[0]) ({cards[0]}), {card_id(cards[1])} ({cards[1]})\n")
                card_visual(cards)
                break
            elif hand:
                cards = hand.split()
                try:
                    cards = [int(c) for c in cards]
                    if (len(cards) != 2 or cards[0] == cards[1]
                            or not (1 <= cards[0] <= 52) or not (1 <= cards[1] <= 52)):
                        raise ValueError

                except ValueError:
                    print("Uh oh! Invalid input.")
                    continue
                print("You selected:\n - ", card_id(cards[0]), " (", cards[0], ")\n - ",
                      card_id(cards[1]), " (", cards[1], ")\n")
                card_visual(cards)
                break
        cards_set = set(cards)
        while 1:
            round_name = None
            com_cards = []
            community_cards = input("Enter 0,3,4, or 5 card integers separated by a space to represent the \n"
                                    "community cards (Ex. '12, 43, 10, 22'). For random community cards, enter\n'0'"
                                    " to begin at the pre-flop, '3' for the flop, '4' for the turn,\n"
                                    " and '5' for the river.")

            if community_cards == '0':
                com_cards = []
                round_name = "Pre-Flop"
                break
            elif community_cards == '3': # Flop
                com_cards = list(get_random_card(3, excluded=cards_set))
                round_name = "Flop"
                break
            elif community_cards == '4': # Turn
                com_cards = list(get_random_card(4, excluded=cards_set))
                round_name = "Turn"
                break
            elif community_cards == '5': # River
                com_cards = list(get_random_card(5, excluded=cards_set))
                round_name = "River"
                break
            else:
                com_cards_str = set(community_cards.split())
                if com_cards_str and len(com_cards_str) not in [0,3,4,5]:
                    print("Invalid input.")
                    continue
                validity_check = True
                for card in com_cards_str:
                    try:
                        card = int(card)
                        if card in cards_set or not 1 <= card <= 52:
                            raise ValueError
                        com_cards.append(card)
                    except ValueError:
                        print(f"Invalid input. Please enter unique integers between 1-52, excluding cards already "
                              f"in your hand ({cards[0]} and {cards[1]}).\n")
                        validity_check = False
                        continue
                if not validity_check:
                    continue
                # Passed checks, continue
                rounds = ["Pre-Flop", "", "", "Flop", "Turn", "River"]
                round_name = rounds[len(com_cards)]
                break

    print("\nBeginning at the", round_name, "...\n")
    print("Your hand:\n", card_id(cards[0]), ", ", card_id(cards[1]))
    card_visual(cards)
    print("Community cards:")
    pnt = ""
    for c in com_cards:
        pnt += card_id(c) + ", "
    print(pnt[:-2])
    card_visual(com_cards)

    # Begin predictions and finish out game, simulating and choosing to stay or fold.
    while len(com_cards) <= 5:
        print(f"Simulation running at the {round_name}.\n")
        print("Predicting for 10 seconds...")

        sim = simulate_rounds(cards, com_cards)
        odds = "stay" if  sim > 0.5 else "fold"

        print(f"Given the odds, PokerBot recommends that you {odds}.")
        while 1:
            decision = input("Stay (s) or fold (f)?")
            if decision.lower() == 'f':
                if sim <= 0.5:
                    print("Great choice!")
                else:
                    print("Hmm. Interesting choice.")
                rabbit_hunting = input("Would you like to see what your opponent had? (y or n)")
                if rabbit_hunting.lower() == 'y':
                    if len(com_cards) != 5:
                        com_cards = com_cards + list(get_random_card(5 - len(com_cards), excluded=cards_set.union(set(com_cards))))
                    winner,opp_hand = poker_round(cards, set(cards).union(com_cards), com_cards)
                    opp_hand = list(opp_hand)
                    print("Your hand:\n", card_id(cards[0]), ", ", card_id(cards[1]))
                    card_visual(cards)
                    print("Community cards:\n")
                    pnt = ""
                    for c in com_cards:
                        pnt += card_id(c) + ", "
                    print(pnt[:-2])
                    card_visual(com_cards)
                    print("Your opponent's hand:\n", card_id(opp_hand[0]), ", ", card_id(opp_hand[1]))
                    card_visual(opp_hand)
                    if winner == 1:
                        if sim > 0.5:
                            print("Rats! Looks like you shouldn't have folded.\n"
                                  " Maybe try listening to me next time?")
                        else:
                            print("Oh no! Looks like we would've won; that one is on me. \n"
                                  "I'll be sure to give you better advice next time.")
                        return
                    else:
                        if sim > 0.5:
                            print("Wow, great fold, well done! You certainly know when to get out of the building!")
                        else:
                            print("Good fold! You were smart to listen to me.")
                        return
                else:
                    print("Better not to know anyways. You're ready for Vegas!")
                    return
            elif decision.lower() == 's': # STAY
                if round_name == "Pre-Flop":
                    round_name = "Flop"
                    com_cards = com_cards + list(get_random_card(3,  excluded=cards_set))

                elif round_name == "Flop":
                    round_name = "Turn"
                    com_cards = com_cards + list(get_random_card(1, excluded=cards_set.union(set(com_cards))))

                elif round_name == "Turn":
                    round_name = "River"
                    com_cards = com_cards + list(get_random_card(1, excluded=cards_set.union(set(com_cards))))

                elif round_name == "River":
                    print("We're in it now. Let's see what your opponent had...")
                    winner,opp_hand = poker_round(cards, set(cards).union(com_cards), com_cards)
                    opp_hand = list(opp_hand)
                    print("Your opponent's hand:\n", card_id(opp_hand[0]), ", ", card_id(opp_hand[1]))
                    card_visual(opp_hand)
                    if winner == 1:
                        if sim > 0.5:
                            print("Look at that! Great win! Looks like you should take my advice more often!")
                        else:
                            print("Wow! Great call! I definitely know who I'm taking to Vegas next time!")
                        return
                    else:
                        if sim > 0.5:
                            print("Yikes. Unlucky loss there. That one is my bad. No, sorry, I will not reimburse you.")
                        else:
                            print("The odds were never in your favor. What am I here for anyways?")
                        return

                print("Community cards:\n")
                pnt = ""
                for c in com_cards:
                    pnt += card_id(c) + ", "
                print(pnt[:-2])
                card_visual(com_cards)
                break

            else:
                print("Invalid choice.")
                continue

if __name__ == '__main__':
    main()