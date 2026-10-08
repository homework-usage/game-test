import random
import time

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"[{self.rank}{self.suit}]"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

def calculate_score(hand):
    score = sum(VALUES[card.rank] for card in hand)
    aces = sum(1 for card in hand if card.rank == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def render_table(player_hand, dealer_hand, hide_dealer=True):
    print("\n" + "=" * 40)
    
    # Dealer Display
    if hide_dealer:
        dealer_str = f"{dealer_hand[0]}  [ ? ]"
        print(f" DEALER'S HAND: {dealer_str}")
        print(" DEALER'S SCORE: ?")
    else:
        dealer_str = "  ".join(str(card) for card in dealer_hand)
        print(f" DEALER'S HAND: {dealer_str}")
        print(f" DEALER'S SCORE: {calculate_score(dealer_hand)}")

    print("-" * 40)

    # Player Display
    player_str = "  ".join(str(card) for card in player_hand)
    print(f" YOUR HAND:   {player_str}")
    print(f" YOUR SCORE:  {calculate_score(player_hand)}")
    print("=" * 40 + "\n")

def play_round():
    deck = Deck()
    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    # Player Turn
    while True:
        render_table(player_hand, dealer_hand, hide_dealer=True)
        player_score = calculate_score(player_hand)

        if player_score == 21:
            print("✨ Blackjack! You hit 21!")
            break
        elif player_score > 21:
            print("💥 Bust! You went over 21. Dealer wins.")
            return

        choice = input("Action: [H]it or [S]tand? ").strip().lower()
        if choice in ['h', 'hit']:
            player_hand.append(deck.draw())
        elif choice in ['s', 'stand']:
            break
        else:
            print("Invalid input. Type 'H' to Hit or 'S' to Stand.")

    # Dealer Turn
    render_table(player_hand, dealer_hand, hide_dealer=False)
    print("Dealer's turn...")
    time.sleep(1)

    while calculate_score(dealer_hand) < 17:
        card = deck.draw()
        dealer_hand.append(card)
        print(f"Dealer draws {card}...")
        time.sleep(1)
        render_table(player_hand, dealer_hand, hide_dealer=False)

    # Outcome Calculation
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if dealer_score > 21:
        print("🎉 Dealer busted! You win!")
    elif dealer_score > player_score:
        print(f"❌ Dealer wins with {dealer_score} vs your {player_score}.")
    elif player_score > dealer_score:
        print(f"🏆 You win with {player_score} vs dealer's {dealer_score}!")
    else:
        print("🤝 It's a tie (Push)!")

def main():
    print("=== WELCOME TO ONLINE PYTHON BLACKJACK ===")
    while True:
        play_round()
        play_again = input("\nPlay another round? (y/n): ").strip().lower()
        if play_again not in ['y', 'yes']:
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
