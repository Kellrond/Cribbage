from enum import Enum
from enum import IntEnum
from random import *

fullDeck = []
playDeck = []
player1cards = []
player2cards = []
crib = []
thePlay = []
dealer = bool
canGo = bool
playCount = 0

# # Card enum for cards
class Card(IntEnum):

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


# # Suit Enum for cards
class Suit(Enum):
    SPADES = 'spades'
    CLUBS = 'clubs'
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'


# # Class to hold card info
class PlayingCard:
    def __init__(self, card_name, card_numb, card_suit, card_value,discard=False):
        self.name = card_name
        self.numb = card_numb
        self.suit = card_suit
        self.value = card_value
        self.discard = discard

    def textPlay(self):
        output = self.name.name.capitalize() + " " + self.suit.name.capitalize()
        return output


def createDeck():
    for suit in Suit:
        for card in Card:
            if card.value > 10:
                cardValue = 10
            else:
                cardValue = card.value
            fullDeck.append(PlayingCard(card, card.value, suit, cardValue))
    shuffle(fullDeck)


# # Draw single card from deck
def cutDeck(deck):
    # input("Hit enter to cut the deck")
    randCard = randint(0, len(deck)-1)
    return deck.pop(randCard)


def cutToStart():

    winnerFound = False
    while not winnerFound:

        createDeck()
        # input("Cut and see who goes first")
        # cutDepth = randint(10, 40)
        # p1cut = fullDeck[cutDepth-1]
        # p2cut = cutDeck(fullDeck[cutDepth + 1:])

        p1cut = fullDeck[randint(0, 26)]
        p2cut = fullDeck[randint(27, 52)]

        if p1cut.numb < p2cut.numb:
            dealer = True
            winnerFound = True
            print("Player 1 cut - ", p1cut.textPlay())
            print("Player 2 cut - ", p2cut.textPlay())
            print("You win!! Your turn to deal")
            
        elif p1cut.numb > p2cut.numb:
            dealer = False
            winnerFound = True
            print("Player 1 cut - ", p1cut.textPlay())
            print("Player 2 cut - ", p2cut.textPlay())
            print("You loose! Computer goes first")
            
        else:
            print("Player 1 cut - ", p1cut.textPlay())
            print("Player 2 cut - ", p2cut.textPlay())
            print("TIE! Draw again")
            winnerFound = False
            
    return dealer


def deal():
    if dealer:
        for i in range(0, 6):
            player1cards.append(playDeck.pop())
            player2cards.append(playDeck.pop())
    else:
        for i in range(0, 6):
            player2cards.append(playDeck.pop())
            player1cards.append(playDeck.pop())


def p1discard():
    # finished = False
    # while not finished:
    #
    #     if len(player1cards) == 4:
    #         finished = True
    #     else:
    #         for index, cards in enumerate(player1cards):
    #             print(index, cards.textPlay())
    #         discard = input("Select first cards to discard")
    #         if int(discard) >= 0 or int(discard) <= 5:
    #             crib.append(player1cards.pop(int(discard)))
    #         else:
    #             print("Please make a valid selection")
    for i in range(0,2):
        randCard = randint(0, len(player1cards) - 1)
        crib.append(player1cards.pop(randCard))


def p2discard():
    for i in range(0,2):
        randCard = randint(0, len(player2cards) - 1)
        crib.append(player2cards.pop(randCard))


def canGo(hand, count):

    cango = False
    for c in hand:
        if c.value + count <= 31:
            cango = True
        else:
            cango = False

    return cango


def playableCards(cards, count):

    playable = []
    for index, c in enumerate(cards):
        if c.value + count <= 31:
            playable.append(index)

    return playable


def p1play(playCount):
    playable = playableCards(p1playhand, playCount)

    randCard = playable[randint(0, len(playable) - 1)]
    playCard = p1playhand.pop(randCard)
    playCount += playCard.value
    print("P1:",playCard.textPlay(),"Count:",playCount)


    return playCard



def p2play(playCount):
    playable = playableCards(p2playhand, playCount)

    randCard = playable[randint(0, len(playable) - 1)]
    playCard = p2playhand.pop(randCard)
    playCount += playCard.value
    print("P2:", playCard.textPlay(), "Count:", playCount)

    return playCard


# # Game starts
print("Game begins \n".upper())
createDeck()
playDeck = list(fullDeck)


dealer = cutToStart()

print()

deal()

p2discard()
p1discard()




print("Player 1")
for cards in player1cards: print(cards.textPlay())
print()
print("Player 2")
for cards in player2cards: print(cards.textPlay())
print()
print("Crib")
for cards in crib: print(cards.textPlay())

print()



# # Prep the play phase
print("Play Phase")
p1playhand = player1cards
p2playhand = player2cards

if dealer:
    p1turn = False
else:
    p1turn = True

playPhaseOver = False
while not playPhaseOver:

    if len(p1playhand) == 0 and len(p2playhand) == 0:
        playPhaseOver = True

    playCount = 0

    p1go = False
    p2go = False
    go = False
    while not go:

        if p1go is True and p2go is True:
            go = True
            print("Go!")
        elif p1turn and canGo(p1playhand, playCount):
            thePlay.append(p1play(playCount))
            p1turn = False
        elif p1turn:
            p1go = True
            p1Turn = False
        elif not p1turn and canGo(p2playhand, playCount):
            thePlay.append(p2play(playCount))
            p1Turn = True
        elif not p1turn:
            p2go = True
            p1Turn = True

print("Play phase over")













