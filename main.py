from enum import Enum
from enum import IntEnum
from random import *
from collections import Counter

fullDeck = []
playDeck = []
thePlay = []
p1score = 0
p2score = 0
dealer = bool
canGo = bool
playCount = 0
roundCounter = 1
WIN = 5



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

    return cango


def playableCards(cardsinhand, count):

    playable = []
    for index, c in enumerate(cardsinhand):
        if c.value + count <= 31:
            playable.append(index)

    return playable


def suggestedCard(cardsinhand, count, thePlay):
    suggestion = None

    if len(thePlay) == 0:
        suggestion = None
    else:
        for index, c in enumerate(cardsinhand):
            samplePlay = thePlay.copy()

            if playPairs(samplePlay.append(c)) > 0:
                suggestion = cardsinhand.pop(index)
            elif c.value + count == 15:
                suggestion = cardsinhand.pop(index)
            elif c.value + count == 31:
                suggestion = cardsinhand.pop(index)
    return suggestion


def p1play(playCount, thePlay):
    playable = playableCards(p1playhand, playCount)
    suggestion = suggestedCard(p1playhand, playCount, thePlay)
    if suggestion is not None:
        playCard = suggestion
    else:
        randCard = playable[randint(0, len(playable) - 1)]
        playCard = p1playhand.pop(randCard)

    playCount += playCard.value
    thePlay.append(playCard)
    print("P1:",playCard.textPlay(),"Count:",playCount)

    return playCount


def p2play(playCount, thePlay):
    playable = playableCards(p2playhand, playCount)
    suggestion = suggestedCard(p2playhand, playCount, thePlay)
    if suggestion is not None:
        playCard = suggestion
    else:
        randCard = playable[randint(0, len(playable) - 1)]
        playCard = p2playhand.pop(randCard)

    playCount += playCard.value
    thePlay.append(playCard)
    print("P2:", playCard.textPlay(), "Count:", playCount)

    return playCount


def checkPlayForPoints(playCount, thePlay):
    count = playCount
    play = thePlay
    score = 0
    if playCount == 15:
        score += 2
        print("15 two")
    elif playCount == 31:
        score += 1
        print("31 for two")
    score += playPairs(thePlay)

    return score


def playPairs(play):
    pairsList = thePlay.copy()
    pairsList.reverse()
    score = 0

    # TODO refine this code
    if Counter(pairsList[0:1]).values() == 2:
        if Counter(pairsList[0:2]).values() == 3:
            if Counter(pairsList[0:3]).values() == 4:
                print("Four of a kind @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                score = 12
            else:
                print("Three of a kind @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                score = 6
        else:
            print("Two of a kind @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            score = 2
    return score







# # Game starts
print("───Game begins".upper())
createDeck()
playDeck = list(fullDeck)


dealer = cutToStart()

print()



# # Prep the play phase
print("───Play Phase")

for i in range(0, 1):
    roundPhaseOver = False
    while not roundPhaseOver:
        print(roundCounter,"────¼─────")
        createDeck()
        playDeck = list(fullDeck)

        player1cards = []
        player2cards = []
        crib = []
        thePlay = []

        deal()

        p2discard()
        p1discard()

        p1playhand = player1cards.copy()
        p2playhand = player2cards.copy()

        if dealer:
            p1turn = False
        else:
            p1turn = True

        if p1turn:
            print("Player 1 starts")
        else:
            print("Player 2 starts")

        outOfCards = False
        while not outOfCards:
            if len(p1playhand) == 0 and len(p2playhand) == 0:
                outOfCards = True
            else:
                playCount = 0
                p1go = False
                p2go = False

                go = False
                while not go:
                    if p1go is True and p2go is True:
                        go = True
                        print("Go!", playCount)
                        if p1turn:
                            p2score += 1
                            print("Player 2 Scores - Total -", p2score)
                        else:
                            p1score += 1
                            print("Player 1 Scores - Total -", p1score)
                        for c in thePlay:
                            print(c.textPlay(), end="\t")
                        print()
                        thePlay = []

                    elif p1turn and canGo(p1playhand, playCount):
                        playCount = p1play(playCount, thePlay)
                        if len(thePlay) > 1:
                            p1score += checkPlayForPoints(playCount, thePlay)
                        p1turn = False
                    elif p1turn:
                        p1go = True

                        p1turn = False
                    elif not p1turn and canGo(p2playhand, playCount):
                        playCount = p2play(playCount, thePlay)
                        if len(thePlay) > 1:
                            p2score += checkPlayForPoints(playCount, thePlay)
                        p1turn = True
                    elif not p1turn:
                        p1turn = True
                        p2go = True

        print()
        print("───Play phase over")

        print("Player 1")
        for cards in player1cards: print(cards.textPlay())
        print()
        print("Player 2")
        for cards in player2cards: print(cards.textPlay())
        print()
        print("Crib")
        for cards in crib: print(cards.textPlay())

        print()
        print("Player 1 Score -", p1score)
        print("Player 2 score -", p2score)
        print("─── Round",roundCounter)

        if dealer:
            dealer = False
        else:
            dealer = True

        if p1score >= WIN or p2score >= WIN:
            roundPhaseOver = True
            with open("Roundtests.txt", "a") as fp:
                fp.write(str(roundCounter) + ", ")
            roundCounter = 0
            p1score = 0
            p2score = 0
        else:
            roundPhaseOver = False
            roundCounter += 1















