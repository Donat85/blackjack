import random
import time

class Deck:
    def __init__(self):
        suits = ["clubs", "hearts", "spades", "diamonds"]
        figures = list(range(2, 11)) + ["J", "Q", "K", "A"]
        self.deck = [(a, b) for a in figures for b in suits]

    def shuffle(self):
        random.shuffle(self.deck)

    def print(self, cards, unknown=False):
        for i, card in enumerate(cards):
            print(" ", end="")
            match card[1]:
                case "clubs":
                    print(str(card[0]) + u"\u2663", end="")
                case "hearts":
                    print(str(card[0]) + u"\u2665", end="")
                case "spades":
                    print(str(card[0]) + u"\u2660", end="")
                case "diamonds":
                    print(str(card[0]) + u"\u2666", end="")
            if i != len(cards)-1:
                print(",", end="")
        if unknown:
            print(", Unknown", end="")
        print("\r")
    
    def get_card(self):
        return self.deck.pop()

    def count(self, hand, ifDealer=False):
        value = 0
        aces = 0
        for card in hand:
            card = card[0]
            if card in ["J", "Q", "K"]:
                value += 10
            elif card == "A":
                aces += 1
            else:
                value += card
        while aces:
            aces -= 1
            if value <= 10 - aces or ifDealer:
                value += 11
            else:
                value += 1
        return value


def allowed_input(text, *args):
    print(text, end=" ")
    inp = input()
    while inp not in args:
        print("That is not a valid option. Try again.")
        print(text, end=" ")
        inp = input()
    return inp

def bet_input(upper_boundary, lower_boundary=1):
    while True:
        print("Place your bet:", end=" ")
        try:
            inp = float(input())
        except:
            print("That is not a valid option. Try again.")
            continue
        if inp > upper_boundary:
            print("You do not have sufficient funds.")
        elif inp < lower_boundary:
            print("The minimum bet is $1.")
        else:
            return inp


if __name__=='__main__':
    print("\nWelcome to Blackjack!")

    vallet = 500.0

    while True:
        print("\n")
        play = allowed_input("You are starting with ${}, would you like to play a hand?".format(vallet), "yes", "no")
        if  play == 'no':
            print("\nYou left the game with ${}.".format(vallet))
            break

        bet = bet_input(vallet)

        deck = Deck()
        deck.shuffle()
        playersHand = [deck.get_card(), deck.get_card()]
        dealersHand = [deck.get_card(), deck.get_card()]
        print("You are dealt:", end=" ")
        deck.print(playersHand)
        time.sleep(0.5)
        print("The dealer is dealt:", end=" ")
        deck.print([dealersHand[0]], unknown=True)
        time.sleep(0.5)

        if deck.count(playersHand)==21:
            print("The dealer has:", end=" ")
            deck.print(dealersHand)
            if deck.count(dealersHand, ifDealer=True) != 21:
                vallet += bet*1.5
                print("Blackjack! You win ${} :)".format(bet*1.5))
                continue
            else:
                print("You tie. Your bet has been returned.")
                continue
        
        while deck.count(playersHand) < 21:
            hitOrStay = allowed_input("Would you like to hit or stay?", "hit", "stay")
            if hitOrStay == "stay":
                break
            newCard = deck.get_card()
            playersHand.append(newCard)
            print("You are dealt:", end=" ")
            deck.print([newCard])
            time.sleep(0.5)
            print("You now have:", end=" ")
            deck.print(playersHand)
            time.sleep(0.5)

        playersValue = deck.count(playersHand)

        if playersValue==21:
            print("The dealer has:", end=" ")
            deck.print(dealersHand)
            if deck.count(dealersHand, ifDealer=True) != 21:
                vallet += bet*1.5
                print("Blackjack! You win ${} :)".format(bet*1.5))
                time.sleep(1)
                continue
            else:
                print("You tie. Your bet has been returned.")
                time.sleep(1)
                continue
        if playersValue > 21:
            print("Your hand value is over 21 and you lose ${} :(".format(bet))
            vallet -= bet
            if vallet == 0:
                print("\nYou've ran out of money. Please restart this program to try again.")
                break
            else:
                time.sleep(1)
                continue
        
        print("The dealer has:", end=" ")
        deck.print(dealersHand)
        time.sleep(0.5)

        while deck.count(dealersHand, ifDealer=True) < 17:
            newCard = deck.get_card()
            dealersHand.append(newCard)
            print("The dealer hits and is dealt:", end=" ")
            deck.print([newCard])
            time.sleep(0.5)
            print("The dealer has:", end=" ")
            deck.print(dealersHand)
            time.sleep(0.5)

        dealersValue = deck.count(dealersHand, ifDealer=True)
        
        if dealersValue > 21:
            print("The dealer busts, you win ${} :)".format(bet))
            vallet += bet
            time.sleep(1)
        elif playersValue > dealersValue:
            print("The dealer stays.")
            print("You win ${}!".format(bet))
            vallet += bet
            time.sleep(1)
        elif dealersValue > playersValue:
            print("The dealer stays.")
            print("The dealer wins, you lose ${} :(".format(bet))
            vallet -= bet
            if vallet == 0:
                print("\nYou've ran out of money. Please restart this program to try again.")
                break
            time.sleep(1)
        else:
            print("You tie. Your bet has been returned.")
            time.sleep(1)

    print("Goodbye")