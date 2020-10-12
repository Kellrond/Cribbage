from enum import Enum
from enum import IntEnum
from random import *
from statistics import mean
import time
from collections import Counter

fullDeck = []
playDeck = []
thePlay = []
p1score = 0
p2score = 0
dealer = bool
playCount = 0
roundCounter = 1
WIN = 121


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


class Suit(Enum):
    SPADES = 'spades'
    CLUBS = 'clubs'
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'


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

# #
# # Deck functions
# #

def createDeck():

    for suit in Suit:
        for card in Card:
            if card.value > 10:
                cardValue = 10
            else:
                cardValue = card.value
            fullDeck.append(PlayingCard(card, card.value, suit, cardValue))
    shuffle(fullDeck)


def cutDeck(deck):

    # input("Hit enter to cut the deck")
    randCard = randint(0, len(deck)-1)
    return deck.pop(randCard)


def cutToStart():

    isDealer = False
    winnerFound = False
    while not winnerFound:

        createDeck()


        p1cut = fullDeck[randint(0, 26)]
        p2cut = fullDeck[randint(27, 52)]

        if p1cut.numb < p2cut.numb:
            isDealer = True
            winnerFound = True
            print("Player 1 cut - ", p1cut.textPlay())
            print("Player 2 cut - ", p2cut.textPlay())
            print("You win!! Your turn to deal")
            
        elif p1cut.numb > p2cut.numb:
            isDealer = False
            winnerFound = True
            print("Player 1 cut - ", p1cut.textPlay())
            print("Player 2 cut - ", p2cut.textPlay())
            print("You loose! Computer goes first")
            
        else:
            print("Player 1 cut - ", p1cut.textPlay())
            print("Player 2 cut - ", p2cut.textPlay())
            print("TIE! Draw again")
            winnerFound = False
            
    return isDealer


def deal():

    shuffle(playDeck)

    if dealer:
        for i in range(0, 6):
            player2cards.append(playDeck.pop())
            player1cards.append(playDeck.pop())
    else:
        for i in range(0, 6):
            player1cards.append(playDeck.pop())
            player2cards.append(playDeck.pop())

# #
# # Player decision function
# #

def p1discard():

    for i in range(0, 2):
        randCard = randint(0, len(player1cards) - 1)
        crib.append(player1cards.pop(randCard))


def p2discard():

    for i in range(0, 2):
        randCard = randint(0, len(player2cards) - 1)
        crib.append(player2cards.pop(randCard))


def canGo(hand):

    cango = False
    for c in hand:
        if c.value + playCount <= 31:
            cango = True

    return cango


def playableCards(cardsInHand):

    playable = []
    for index, c in enumerate(cardsInHand):
        if c.value + playCount <= 31:
            playable.append(index)

    return playable


def suggestedCard(cardsInHand):

    suggestion = None
    if len(thePlay) == 0:
        # # Todo add card suggestion
        suggestion = None
    else:
        for index, c in enumerate(cardsInHand):
            if testRuns(c):
                suggestion = cardsInHand.pop(index)
                break
            elif testPairs(c):
                suggestion = cardsInHand.pop(index)
                break
            elif c.value + playCount == 15:
                suggestion = cardsInHand.pop(index)
            elif c.value + playCount == 31:
                suggestion = cardsInHand.pop(index)
    return suggestion


def testPairs(testCard):
    lastPlayed = thePlay[len(thePlay)-1]
    if lastPlayed.numb == testCard.numb:
        return True
    else:
        return False


def testRuns(testCard):

    hasRun = False
    index = len(thePlay)
    if index > 1 and not hasRun:
        for i in range(3, index+1):
            evalCards = thePlay[index - i:index].copy()
            evalCards.append(testCard)
            cardNumbList = []
            for l in evalCards:
                cardNumbList.append(l.numb)
            sortedCards = sorted(cardNumbList)
            rangeList = list(range(min(sortedCards),max(sortedCards)+1))

            if sortedCards == rangeList:
                print("Has Run")
                hasRun = True
            else:
                pass
    else:
        pass

    return hasRun

# #
# # Player action functions
# #

def p1play():

    playable = playableCards(p1playhand)
    suggestion = suggestedCard(p1playhand)
    if suggestion is not None:
        playCard = suggestion
    else:
        randCard = playable[randint(0, len(playable) - 1)]
        playCard = p1playhand.pop(randCard)

    addCount = playCard.value
    thePlay.append(playCard)

    spc = 14 - len(playCard.textPlay())
    print("P1:", playCard.textPlay(), " " * spc, "     Count:", addCount + playCount)

    return addCount

def p2play():

    playable = playableCards(p2playhand)
    suggestion = suggestedCard(p2playhand)
    if suggestion is not None:
        playCard = suggestion
    else:
        randCard = playable[randint(0, len(playable) - 1)]
        playCard = p2playhand.pop(randCard)

    addCount = playCard.value
    thePlay.append(playCard)

    spc = 14 - len(playCard.textPlay())
    print("P2:", playCard.textPlay(), " " * spc, "     Count:", addCount + playCount)

    return addCount


def checkPlayForPoints():
    count = playCount
    play = thePlay
    score = 0
    if playCount == 15:
        score += 2
        print("15 two")
    elif playCount == 31:
        score += 1
        print("31 for two")
    score += playPairs()
    score += playRuns()

    return score


def playPairs():
    pairsList = thePlay.copy()
    pairsList.reverse()
    pairsValueList = []
    for c in pairsList:
        pairsValueList.append(c.numb)

    score = 0

    # TODO refine this code

    onePair = len(set(pairsValueList[0:2]))
    twoPair = len(set(pairsValueList[0:3]))
    thrPair = len(set(pairsValueList[0:4]))

    if onePair == 1:
        if twoPair == 1 and len(pairsValueList) > 2:
            if thrPair == 1 and len(pairsValueList) > 3:
                print(" Four of a kind")
                score = 12
            else:
                print(" Three of a kind")
                score = 6
        else:
            print(" Two of a kind")
            score = 2
    else:
        pass
    return score


def playRuns():

    score = 0
    scoreList = [0]
    index = len(thePlay)
    if index > 2:
        for i in range(3, index+1):
            evalCards = thePlay[index - i:index].copy()
            cardNumbList = []
            for l in evalCards:
                cardNumbList.append(l.numb)
            sortedCards = sorted(cardNumbList)
            rangeList = list(range(min(sortedCards),max(sortedCards)+1))

            if sortedCards == rangeList:
                print("Run of", i)
                scoreList.append(i)
            else:
                pass

    else:
        score = 0
    score = max(scoreList)
    return score

# # Test functions
AVG_TEST = []
START = time.time()

# #
# # Game starts
# #


for i in range(0, 100):

    print("─────────────── GAME BEGINS ───────────────".upper())
    createDeck()
    playDeck = list(fullDeck)

    dealer = cutToStart()

    roundPhaseOver = False
    while not roundPhaseOver:
        print()
        print()
        print("───────────", roundCounter, "BEGINS ────────────")

        player1cards = []
        player2cards = []
        crib = []
        thePlay = []
        fullDeck = []
        playDeck = []

        createDeck()
        playDeck = list(fullDeck)

        # # Play begins
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
            print("                   PLAYER 1 STARTS")
        else:
            print("                   PLAYER 2 STARTS")

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
                        if p1turn:
                            p2score += 1
                            print("GO!! Player 2 Scores ")
                        else:
                            p1score += 1
                            print("GO!! Player 1 Scores ")
                        print()
                        thePlay = []

                    elif p1turn and canGo(p1playhand):
                        playCount += p1play()
                        if len(thePlay) > 1:
                            p1score += checkPlayForPoints()
                        p1turn = False
                    elif p1turn:
                        p1go = True
                        p1turn = False
                    elif not p1turn and canGo(p2playhand):
                        playCount += p2play()
                        if len(thePlay) > 1:
                            p2score += checkPlayForPoints()
                        p1turn = True
                    elif not p1turn:
                        p1turn = True
                        p2go = True

        print("Player 1 Score -", p1score)
        print("Player 2 score -", p2score)
        print("────────────────────── HANDS ─────")

        print("Player 1")
        for cards in player1cards: print(cards.textPlay())
        print()
        print("Player 2")
        for cards in player2cards: print(cards.textPlay())
        print()
        print("Crib")
        for cards in crib: print(cards.textPlay())

        if dealer:
            dealer = False
        else:
            dealer = True

        if p1score >= WIN or p2score >= WIN:
            roundPhaseOver = True

            # # Test function
            with open("Roundtests.txt", "a") as fp:
                fp.write(str(roundCounter) + ", ")
            AVG_TEST.append(roundCounter)

            roundCounter = 0
            p1score = 0
            p2score = 0
        else:
            roundPhaseOver = False
            roundCounter += 1


# # Test Functions
END = time.time()
DURATION = END - START

print("Average Rounds", mean(AVG_TEST))
print("Duration", DURATION)












