import pygame, sys, random, copy
from pygame.locals import *
from cards import *

def genCard(cList, xList):
    #Generate and remove an card from cList and append it to xList.
    #Return the card, and whether the card is an Ace
    cA = 0
    card = random.choice(cList) #Keeps on generating same random card for the cList
    cList.remove(card)
    xList.append(card)
    if card in cardA:
        cA = 1
    return card, cA

def initGame(cList, uList, dList):
    #Generates two cards for dealer and user, one at a time for each.
    #Returns if card is Ace and the total amount of the cards per person.
    userA = 0
    dealA = 0
    card1, cA = genCard(cList, uList)
    userA += cA
    card2, cA = genCard(cList, dList)
    dealA += cA
    dealAFirst = copy.deepcopy(dealA)
    card3, cA = genCard(cList, uList)
    userA += cA
    card4, cA = genCard(cList, dList)
    dealA += cA
    #The values are explained below when calling the function
    return getAmt(card1) + getAmt(card3), userA, getAmt(card2) + getAmt(card4), dealA, getAmt(card2), dealAFirst

def make_state(userSum, userA, dealFirst, dealAFirst):
    #Eliminate duplicated bust cases
    if userSum > 21: 
        userSum = 22
    #userSum: sum of user's cards
    #userA: number of user's Aces
    #dealFirst: value of dealer's first card
    #dealAFirst: whether dealer's first card is Ace   
    return (userSum, userA, dealFirst, dealAFirst)

#Runs the policy from the current state. If doOnce is true, terminate after one iteration
def simulateSequence(state, cList, doOnce):
    sequence = [state]
    userSum = state[0]
    userA = state[1]
    while userSum < 17:
        card, cA = genCard(cList, [])   #Can I let xList be empty?
        userA += cA
        userSum += getAmt(card)
        while userSum > 21 and userA > 0:
            userA -= 1
            userSum -= 10
        sequence.append(make_state(userSum, userA, state[2], state[3]))
        #True for TD Learning
        if doOnce:
            break
    return sequence

#Simulate an action from the state. If action == 1 stand, otherwise hit
def simulateAction(state, cList, action):
    if action == 1: #Stand
        return state

    userSum = state[0]
    userA = state[1]
    card, cA = genCard(cList, [])  
    userA += cA
    userSum += getAmt(card)
    while userSum > 21 and userA > 0:
        userA -= 1
        userSum -= 10
    return make_state(userSum, userA, state[2], state[3])

#Gets reward for current state by simulating the remaining dealers card and compare values
def getReward(state, cList, dealSum, dealA):
    userSum = state[0]
    while dealSum <= userSum and dealSum < 17:
        card, cA = genCard(cList, [])
        dealA += cA
        dealSum += getAmt(card)
        while dealSum > 21 and dealA > 0:
            dealA -= 1
            dealSum -= 10
    if userSum <= 21 and dealSum < userSum or dealSum > 21:
        return 1
    elif userSum == dealSum: #Draw return 0
        return 0
    else:
        return -1

#Returns 0 for hit and 1 for stand
def pickAction(state, eps, Q):
    if random.random() < eps:
        return random.randint(0,1)
    else:
        if Q[state][0] >= Q[state][1]:
            return 0
        else:
            return 1

def main():
    ccards = copy.copy(cards)
    stand = False
    userCard = []
    dealCard = []
    winNum = 0
    loseNum = 0
    #Initialize Game
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Blackjack')
    font = pygame.font.SysFont("", 20)
    hitTxt = font.render('Hit', 1, black)
    standTxt = font.render('Stand', 1, black)
    restartTxt = font.render('Restart', 1, black)
    MCTxt = font.render('MC', 1, blue)
    TDTxt = font.render('TD', 1, blue)
    QLTxt = font.render('QL', 1, blue)
    gameoverTxt = font.render('End of Round', 1, white)
    #Prepare table of utilities
    MCvalues = {}
    MCGvalues = {}
    visitsT = {}
    TDvalues = {}
    Qvalues = {}
    visitsQ = {}
    #i iterates through the sum of user's cards. It is set to 22 if the user went bust. 
    #j iterates through the value of the dealer's first card. Ace is eleven. 
    #a1 is the number of Aces that the user has.
    #a2 denotes whether the dealer's first card is Ace. 
    for i in range(2,23):
        for j in range(2,12):
            for a1 in range(0,5):
                for a2 in range(0,2):
                    s = (i,a1,j,a2)
                    #utility computed by MC-learning
                    MCvalues[s] = 0
                    MCGvalues[s] = []
                    #utility computed by TD-learning
                    TDvalues[s] = 0
                    visitsT[s] = 0
                    #first element is Q value of "Hit", second element is Q value of "Stand"
                    Qvalues[s] = [0,0]
                    visitsQ[s] = 0
    #userSum: sum of user's cards
    #userA: number of user's Aces
    #dealSum: sum of dealer's cards (including hidden one)
    #dealA: number of all dealer's Aces, 
    #dealFirst: value of dealer's first card
    #dealAFirst: whether dealer's first card is Ace
    userSum, userA, dealSum, dealA, dealFirst, dealAFirst = initGame(ccards, userCard, dealCard)
    state = make_state(userSum, userA, dealFirst, dealAFirst)
    #Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((80, 150, 15))
    hitB = pygame.draw.rect(background, gray, (10, 445, 75, 25))
    standB = pygame.draw.rect(background, gray, (95, 445, 75, 25))
    MCB = pygame.draw.rect(background, white, (180, 445, 75, 25))
    TDB = pygame.draw.rect(background, white, (265, 445, 75, 25))
    QLB = pygame.draw.rect(background, white, (350, 445, 75, 25))
    autoMC = False
    autoTD = False
    autoQL = False
    #Event loop
    while True:
        #Our state information does not take into account of number of cards
        #So it's ok to ignore the rule of winning if getting 5 cards without going bust
        if (userSum >= 21 and userA == 0) or len(userCard) == 5:
            gameover = True
        else:
            gameover = False
        if len(userCard) == 2 and userSum == 21:
            gameover = True
        if autoMC:
            #MC Learning
            #Compute the utilities of all states under the policy "Always hit if below 17"
            simUserCard = []
            simDealCard = []
            simCards = copy.copy(cards)
            userSum_s, userA_s, dealSum_s, dealA_s, dealFirst_s, dealAFirst_s = initGame(simCards, simUserCard, simDealCard)
            randomState = make_state(userSum_s, userA_s, dealFirst_s, dealAFirst_s)

            sequence = simulateSequence(randomState, simCards, False) 
            reward = getReward(sequence[-1], simCards, dealSum_s, dealA_s)

            #Set values for every simulated state
            for s in reversed(sequence):
                MCGvalues[s].append(reward)
                MCvalues[s] = float(sum(MCGvalues[s])) / max(len(MCGvalues[s]), 1)
                reward *= .9 

        if autoTD:  #Check shared variables
            #TD Learning (erase the dummy +1 of course)
            #Compute the utilities of all states under the policy "Always hit if below 17"
            simUserCard = []
            simDealCard = []
            simCards = copy.copy(cards)
            userSum_s, userA_s, dealSum_s, dealA_s, dealFirst_s, dealAFirst_s = initGame(simCards, simUserCard, simDealCard)
            
            s = make_state(userSum_s, userA_s, dealFirst_s, dealAFirst_s)
            while True:
                sequence = simulateSequence(s, simCards, True)  
                visitsT[s] += 1
                nextS = sequence[-1]
                alpha = 10/(9+visitsT[s])

                #Reached terminal
                if s == nextS:
                    reward = getReward(nextS, simCards, dealSum_s, dealA_s)
                    TDvalues[s] += alpha * (0 + .9 * reward - TDvalues[s])
                    break
                else:
                    TDvalues[s] += alpha * (0 + .9 * TDvalues[nextS] - TDvalues[s]) #Non-terminal reward is 0
                s = nextS

        if autoQL:
            #Q-Learning (erase the dummy +1 of course)
            #For each state, compute the Q value of the action "Hit" and "Stand"
            simUserCard = []
            simDealCard = []
            simCards = copy.copy(cards)
            userSum_s, userA_s, dealSum_s, dealA_s, dealFirst_s, dealAFirst_s = initGame(simCards, simUserCard, simDealCard)
            
            s = make_state(userSum_s, userA_s, dealFirst_s, dealAFirst_s)
            eps = .5
            while True:  #Need better way to determine if this is a terminal or not.
                visitsQ[s] += 1
                alpha = 10/(9+visitsQ[s])
                a = pickAction(s, eps, Qvalues)
                nextS = simulateAction(s, simCards, a)
                
                #Reached terminal
                if s == nextS or nextS[0] > 21:
                    reward = getReward(nextS, simCards, dealSum_s, dealA_s)
                    Qvalues[s][a] += alpha * (0 + .9 * reward - Qvalues[s][a])
                    break
                else:
                    Qvalues[s][a] += alpha * (0 + .9 * max(Qvalues[nextS]) - Qvalues[s][a]) #Non-terminal reward is 0
                s = nextS


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Clicking the white buttons can start or pause the learning processes
            elif event.type == pygame.MOUSEBUTTONDOWN and MCB.collidepoint(pygame.mouse.get_pos()):
                autoMC = not autoMC
            elif event.type == pygame.MOUSEBUTTONDOWN and TDB.collidepoint(pygame.mouse.get_pos()):
                autoTD = not autoTD
            elif event.type == pygame.MOUSEBUTTONDOWN and QLB.collidepoint(pygame.mouse.get_pos()):
                autoQL = not autoQL
            elif event.type == pygame.MOUSEBUTTONDOWN and (gameover or stand):
                #restarts the game, updating scores
                if userSum == dealSum:
                    pass
                elif userSum <= 21 and len(userCard) == 5:
                    winNum += 1
                elif userSum <= 21 and dealSum < userSum or dealSum > 21:
                    winNum += 1
                else:
                    loseNum += 1
                gameover = False
                stand = False
                userCard = []
                dealCard = []
                ccards = copy.copy(cards)
                userSum, userA, dealSum, dealA, dealFirst, dealAFirst = initGame(ccards, userCard, dealCard)
            elif event.type == pygame.MOUSEBUTTONDOWN and not (gameover or stand) and hitB.collidepoint(pygame.mouse.get_pos()):
                #Give player a card
                card, cA = genCard(ccards, userCard)
                userA += cA
                userSum += getAmt(card)
                while userSum > 21 and userA > 0:
                    userA -= 1
                    userSum -= 10
            elif event.type == pygame.MOUSEBUTTONDOWN and not gameover and standB.collidepoint(pygame.mouse.get_pos()):
                #Dealer plays, user stands
                stand = True
                if dealSum == 21:
                    pass
                else:
                    while dealSum <= userSum and dealSum < 17:
                        card, cA = genCard(ccards, dealCard)
                        dealA += cA
                        dealSum += getAmt(card)
                        while dealSum > 21 and dealA > 0:
                            dealA -= 1
                            dealSum -= 10
        state = make_state(userSum, userA, dealFirst, dealAFirst)
        MCU = font.render('MC-Utility of Current State: %f' % MCvalues[state], 1, black)
        TDU = font.render('TD-Utility of Current State: %f' % TDvalues[state], 1, black)
        QV = font.render('Q values: (Hit) %f (Stand) %f' % tuple(Qvalues[state]) , 1, black)
        winTxt = font.render('Wins: %i' % winNum, 1, white)
        loseTxt = font.render('Losses: %i' % loseNum, 1, white)
        screen.blit(background, (0, 0))
        screen.blit(hitTxt, (39, 448))
        screen.blit(standTxt, (116, 448))
        screen.blit(MCTxt, (193, 448))
        screen.blit(TDTxt, (280, 448))
        screen.blit(QLTxt, (357, 448))
        screen.blit(winTxt, (550, 423))
        screen.blit(loseTxt, (550, 448))
        screen.blit(MCU, (20, 200))
        screen.blit(TDU, (20, 220))
        screen.blit(QV, (20, 240))
        for card in dealCard:
            x = 10 + dealCard.index(card) * 110
            screen.blit(card, (x, 10))
        screen.blit(cBack, (120, 10))
        for card in userCard:
            x = 10 + userCard.index(card) * 110
            screen.blit(card, (x, 295))
        if gameover or stand:
            screen.blit(gameoverTxt, (270, 200))
            screen.blit(dealCard[1], (120, 10))
        pygame.display.update()

if __name__ == '__main__':
    main()

