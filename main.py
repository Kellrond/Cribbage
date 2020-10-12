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

# ##
# # Deck functions
# ##


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

# ##
# # Player decision function
# ##


def p1discard():

    suggestedDiscard(player1cards)
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


def suggestedDiscard(hand):
    possibleHands = []

    for i in range(0, 6):
        tempHand = hand.copy()
        tempHand.pop(i)
        for j in range(0, 5):
            tempHand2 = tempHand.copy()
            tempHand2.pop(j)
            if j >= i:
                possibleHands.append(tempHand2)

    for pos in possibleHands:
        presortedPos = []
        for c in pos:
            presortedPos.append(c.numb)

        sortedPos = sorted(presortedPos)

        score = 0
        score += countFourCardFlush(pos)
        score += countPairs(pos)

        # # 4 Card run test
        fourCardFound = False
        rangeList = list(range(min(sortedPos), max(sortedPos)+1))
        if sortedPos == rangeList:
            score += 4
            fourCardFound = True

        # # 3 Card run test
        if not fourCardFound:
            for k in range(0, 4):
                tempHand = sortedPos.copy()
                tempHand.pop(k)
                rangeList = list(range(min(tempHand), max(tempHand) + 1))
                if tempHand == rangeList:
                    score += 3

        # # 15's test
        convertHand = pos.copy()
        fifteensHand = []
        for c in convertHand:
            fifteensHand.append(c.value)

        # # 4 Card 15
        if sum(fifteensHand) == 15:
            score += 2

        # # 3 Card 15
        for index, c in enumerate(fifteensHand):
            tempHand = fifteensHand.copy()
            tempHand.pop(index)
            if sum(tempHand) == 15:
                score += 2

        # # 2 Card 15
        for l in range(0, 4):
            tempHand = fifteensHand.copy()
            tempHand.pop(l)
            for m in range(0,3):
                tempHand2 = tempHand.copy()
                tempHand2.pop(m)
                if m >= l:
                    if sum(tempHand2) == 15:
                        score += 2

        print(score, "  ", end="")
        for k in pos:
            print(k.textPlay(), end=" ")
        print()




# ##
# # Player action functions
# ##


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
    spc2 = 2 - len(str(playCount + addCount))
    print("P1:", playCard.textPlay(), " " * spc, "     Count:", addCount + playCount," " * spc2 ,"  Prev Score:", p1score)

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
    spc2 = 2 - len(str(playCount + addCount))
    print("P2:", playCard.textPlay(), " " * spc, "     Count:", addCount + playCount, " " * spc2,"  Prev Score:",p2score)

    return addCount


def checkPlayForPoints():

    score = 0
    if len(thePlay) > 1:
        if playCount == 15:
            score += 2
            print("         15 two")
        elif playCount == 31:
            score += 1
            print("         31 for two")

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
                print("         Four of a kind")
                score = 12
            else:
                print("         Three of a kind")
                score = 6
        else:
            print("         Two of a kind")
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
                print("         Run of", i)
                scoreList.append(i)
            else:
                pass

    else:
        score = 0
    score = max(scoreList)
    return score

# ##
# # Count functions
# ##


def countHand(inHand, isCrib=False):

    score = 0
    hand = inHand.copy()

    flush = countFourCardFlush(hand)
    if flush != 0:
        if hand[0].suit == cut.suit:
            flush += 1
            print("5 Card flush")
    if not isCrib:
        score += flush
    else:
        if flush == 5:
            score += flush

    hand.append(cut)

    sortedHand = []
    for c in hand:
        sortedHand.append(c.numb)
    sortedHand = sorted(sortedHand)

    runs = countFiveCardRun(sortedHand)
    if runs != 0:
        score += runs
        print("FIVE CARD RUN")
    else:
        runs = countFourCardRun(sortedHand)
        if runs != 0:
            score += runs
            if score == 4:
                print("FOUR CARD RUN")
            elif score == 8:
                print("DOUBLE FOUR CARD RUN")
        else:
            runs = countThreeCardRun(sortedHand)
            if runs != 0:
                score += runs
                if score == 3:
                    print("THREE CARD RUN")
                elif score == 6:
                    print("DOUBLE THREE CARD RUN")
                elif score == 9:
                    print("TRIPLE THREE CARD RUN")
                elif score == 12:
                    print("QUADRUPLE THREE CARD RUN")

    pairs = countPairs(hand)

    if pairs == 2:
        print("ONE PAIR")
    elif pairs == 4:
        print("TWO PAIRS")
    elif pairs == 6:
        print("THREE PAIRS")
    elif pairs == 8:
        print("FOUR PAIRS")
    elif pairs == 12:
        print("SIX PAIRS")
    score += pairs

    fifteens = countFifteens(hand)
    if fifteens > 0:
        print("FIFTEEN", fifteens)
    score += fifteens

    for c in inHand:
        if c.numb == 11 and c.suit == cut.suit:
            score += 1
            print("NOBS")

    return score


def countFourCardFlush(hand):

    flushTest = []
    for c in hand:
        flushTest.append(c.suit)
    test = len(set(flushTest))
    if test == 1:
        return 4
    else:
        return 0


def countFiveCardRun(sortedHand):

    rangeList = list(range(min(sortedHand),max(sortedHand)+1))
    if sortedHand == rangeList:
        return 5
    else:
        return 0


def countFourCardRun(sortedHand):

    score = 0

    for i in range(0,len(sortedHand)):
        tempHand = sortedHand.copy()
        tempHand.pop(i)

        rangeList = list(range(min(tempHand), max(tempHand)+1))
        if tempHand == rangeList:
            score += 4
        else:
            pass

    return score


def countThreeCardRun(sortedHand):

    score = 0

    for i in range(0, 5):
        tempHand = sortedHand.copy()
        tempHand.pop(i)
        for j in range(0,4):
            tempHand2 = tempHand.copy()
            tempHand2.pop(j)
            if j >= i:
                rangeList = list(range(min(tempHand2), max(tempHand2)+1))
                if tempHand2 == rangeList:
                    score += 3
    return score


def countPairs(hand):

    score = 0
    tempHand = hand.copy()
    length = len(tempHand)
    for i in range(0, length):
        card1 = tempHand.pop(0)
        for j in range(0, len(tempHand)):
            tempHand2 = tempHand.copy()
            card2 = tempHand2.pop(j)

            if card1.numb == card2.numb:
                score += 2

    return score


def countFifteens(hand):

    score = 0
    convertHand = hand.copy()
    fifteensHand = []

    for c in convertHand:
        fifteensHand.append(c.value)

    # # 5 Card 15
    if sum(fifteensHand) == 15:
        score += 2
        return score

    # # 4 Card 15
    for index, c in enumerate(fifteensHand):
        tempHand = fifteensHand.copy()
        tempHand.pop(index)
        if sum(tempHand) == 15:

            score += 2

    # # 3 Card 15
    for i in range(0, 5):
        tempHand = fifteensHand.copy()
        tempHand.pop(i)
        for j in range(0,4):
            tempHand2 = tempHand.copy()
            tempHand2.pop(j)
            if j >= i:
                if sum(tempHand2) == 15:
                    score += 2

    # # 2 Card 15
    for i in range(0, 5):
        tempHand = fifteensHand.copy()
        tempHand.pop(i)
        for j in range(0,4):
            tempHand2 = tempHand.copy()
            tempHand2.pop(j)
            if j >= i:
                for k in range(0,3):
                    tempHand3 = tempHand2.copy()
                    tempHand3.pop(k)
                    if k >= j:
                        if sum(tempHand3) == 15:
                            score += 2

    return score



# # Test functions
AVG_TEST = []
START = time.time()

# ##
# # Game starts
# ##


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

        # ##
        # # Play Phase loop begins
        # ##

        cut = cutDeck(playDeck)
        print("Cut is a", cut.textPlay())

        if cut.numb == 11:
            if dealer:
                p1score += 1
                print("Player 1 gets Nibs")
            else:
                p2score += 1
                print("Player 2 gets Nibs")

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
                            print("         GO!! Player 2 Scores ")
                        else:
                            p1score += 1
                            print("         GO!! Player 1 Scores ")
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

        # ##
        # # Count begins
        # ##

        print("─── Player 1 Hand")
        p1score += countHand(player1cards)
        print("─── Player 2 Hand")
        p2score += countHand(player2cards)
        print("─── Crib Hand")
        if dealer:
            p1score += countHand(crib, isCrib=True)
        else:
            p2score += countHand(crib, isCrib=True)

        print("────────────────────── HANDS ─────")

        print("Cut is a ", cut.textPlay())
        print("Player 1")
        for cards in player1cards: print(cards.textPlay())
        print()
        print("Player 2")
        for cards in player2cards: print(cards.textPlay())
        print()
        print("Crib")
        for cards in crib: print(cards.textPlay())

        # #
        # # End round and start loop over
        # #

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



