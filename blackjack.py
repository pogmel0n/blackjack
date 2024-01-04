import random

DECK_NO = 1

parser = {
        'J' : 10,
        'Q': 10,
        'K': 10,
        'A': 1
        }


class Deck:
    def __init__(self) -> None:
        self.cards = {key: 4 * DECK_NO for key in range(2, 10)}
        self.cards.update({'J': 4 * DECK_NO, 'Q': 4 * DECK_NO, 'K': 4 * DECK_NO, 'A': 4 * DECK_NO})

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
    '''takes hand and returns total'''
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

def win(player_total: int, deck: Deck) -> None:
    if player_total > 21:
        print("Bust!")
        return

    dealer_hand = []

    while total(dealer_hand) < 17:
        dealer_hand.append(deck.hit())

        print_hand(dealer_hand, False)
    
    print()

    if player_total < total(dealer_hand) and total(dealer_hand) < 22:
        print("You lose")
        return
    elif player_total == total(dealer_hand):
        print("Stand-off")
        return
    else:
        print("You win!")
        return

def print_hand(hand: list, player: bool):
    s = "your hand" if player else "dealer's hand"
    print(f"{s}: ", end="")
    for card in hand:
        print(card, end=" ")
    print()


def main():
    print("Welcome to Blackjack! \n")
    deck = Deck()
    while True:
        player_hand = [deck.hit(), deck.hit()]

        while total(player_hand) < 21:
            print_hand(player_hand, True)

            option = input("'h' to hit or 's' to stand: ")

            print()

            if option == 'h':
                player_hand.append(deck.hit())
            elif option == 's':
                break

        print_hand(player_hand, True)
        print()
        win(total(player_hand), deck)

        replay = input("replay? (y)es or (n)o: ")
        print("------------------------------------------")
        if replay in ["no", "n"]:
            break
            
if __name__ == "__main__":
    main()
