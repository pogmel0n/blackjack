import random

DECK_NO = 1

parser = {"J": 10, "Q": 10, "K": 10, "A": 1}


class Deck:
    def __init__(self) -> None:
        self.cards = {key: 4 * DECK_NO for key in range(2, 10)}
        self.cards.update(
            {"J": 4 * DECK_NO, "Q": 4 * DECK_NO, "K": 4 * DECK_NO, "A": 4 * DECK_NO}
        )

    def available_cards(self):
        cards = []
        for key in self.cards:
            if self.cards[key] != 0:
                cards.append(key)
        return cards

    def hit(self):
        cards = self.available_cards()
        card = random.choice(cards)
        self.cards[card] -= 1
        return card


def total(hand: list) -> int:
    """takes hand and returns total"""
    cards = []
    for card in hand:
        if type(card) != int:
            cards.append(parser[card])
        else:
            cards.append(card)

    total = 0

    for card in sorted(cards, reverse=True):
        if card == 1:
            if 11 + total > 21:
                total += card
            else:
                total += 11
        else:
            total += card
    return total


def win(player_total: int, dealer_total: int) -> tuple:
    '''checks win condition'''
    if player_total > 21:
        return ('Bust!', -1)
    if player_total < dealer_total and dealer_total < 22:
        return ('You lose!', -1)
    elif player_total == dealer_total:
        return ('Tie!', 0)
    else:
        return ('You win!', 1)

def gen_dealer(deck, dealer_card):
    '''generates a hand for the dealer (following the blackjack rules)''' 
    dealer_hand = [dealer_card]

    while total(dealer_hand) < 17:
        dealer_hand.append(deck.hit())

        print_hand(dealer_hand, False)

    return (dealer_hand, total(dealer_hand))

def print_hand(hand: list, player = True):
    '''prints hands prettily''' 
    s = "your hand" if player else "dealer's hand"
    print(f"{s}: ", end="")
    for card in hand:
        print(card, end=" ")
    print()

def split_cards(card, deck, dealer_card):
    '''deals with splitting cards'''
    hand_1 = [card]
    hand_2 = [card]

    split = True
    while split:
        print("1", end=" ")
        print_hand(hand_1)

        print("2", end=" ")
        print_hand(hand_2)

        option = input("'1' to hit on hand 1 and '2' to hit on hand 2, or 's' to stand: ")
        
        if option == '1' and total(hand_1) < 22:
            hand_1.append(deck.hit())
        elif option == '2' and total(hand_2) < 22:
            hand_2.append(deck.hit())
        elif option == 's':
            break

        print()

    split_win(hand_1, hand_2, deck, dealer_card)

def split_win(hand1, hand2, deck, dealer_card):
    '''win condition for split'''
    dealer = gen_dealer(deck, dealer_card)
    print_hand(dealer[0], False)

    win1 = win(total(hand1), dealer[1])
    win2 = win(total(hand2), dealer[1])

    print("Hand 1: ", win1)
    print("Hand 2: ", win2)

def main():
    print("Welcome to Blackjack! \n")
    print("Your starting balance is 69, 420")
    balance = 69420
    
    deck = Deck()
    while True and balance > 0:
        # betting
        bet = 0
        while bet > 100 and bet < balance:
            bet = int(input("Place a bet (minimum 100)"))
        
        dealer_card = deck.hit()
        print(f"dealer's card: {dealer_card}\n")
        player_hand = [deck.hit(), deck.hit()]

        # splitting cards
        if player_hand[0] == player_hand[1]:
            s = input(f"Split {player_hand[0]}s? (y)es or (n)o: ")
            if s.lower() in ["yes", "y"]:
                split_cards(player_hand[0], deck, dealer_card)

        # normal
        else:
            while total(player_hand) < 21:
                print_hand(player_hand)

                option = input("'h' to hit or 's' to stand: ")

                print()

                if option == "h":
                    player_hand.append(deck.hit())
                elif option == "s":
                    break

            print_hand(player_hand)
            print()
            
            # win condition
            dealer = gen_dealer(deck, dealer_card)
            w = win(total(player_hand), dealer[1])
            balance += (bet * w[1])
            print(w[0])

            # replay
            replay = input("replay? (y)es or (n)o: ")
            if replay.lower() in ["no", "n"]:
                break

            print("------------------------------------------")

            # shuffle
            if len(deck.available_cards()) < 10:
                print("Shuffling... \n")
                deck = Deck()

if __name__ == "__main__":
    main()
