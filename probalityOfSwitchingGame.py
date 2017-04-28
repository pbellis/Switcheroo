cache = {0:(0.0,0)}
import random

def probalisticSwitching(chips,subtractionSet,p):
    if chips in cache:
        return cache[chips]
    else:
        possiblePositions = [(s,chips-s) for s in subtractionSet if (chips-s)>=0]#calculate the possible positions
        possibleProbabilitiesIfSucess = [(position[0],probalisticSwitching(position[1],subtractionSet,p)[1]) for position in possiblePositions]
        probabilityWinWithS = [(probSucess[0],(((1-probSucess[1])*(1-p))+probSucess[1]*p)) for probSucess in possibleProbabilitiesIfSucess]
        bestTakeAway = max(probabilityWinWithS,key=lambda x:x[1])
        cache[chips]=bestTakeAway
        return bestTakeAway

def strategicAI(chips,subtractionSet,p):
    return probalisticSwitching(chips,subtractionSet,p)[0]

def randomAI(chips,subtractionSet,p):
    return random.sample(subtractionSet,1)[0]


def game(numberOfChips,subtractionSet,p,P1,P2):#player 1 starts, pass a method that returns an int in the subtraction set from the input of chips,subtractionset,p
    p1Turn = True
    while(numberOfChips>0):
        if(p1Turn):
            p1Move = P1(numberOfChips,subtractionSet,p)
            numberOfChips=max(numberOfChips-p1Move,0)#don't go below zero but subtract the players move
        else:
            p2Move = P2(numberOfChips,subtractionSet,p)
            numberOfChips=max(numberOfChips-p2Move,0)#don't go below zero but subtract the players move
        
        if(random.random()>p):
            p1Turn = not p1Turn
    return p1Turn # true if p1 loses, false if p1 wins

            
    

def trials(trials,numberOfChips,subtractionSet,p,P1,P2):
    p1Wins = 0
    for i in range(trials):
        if(not game(numberOfChips,subtractionSet,p,P1,P2)):#p1 wins 
            p1Wins+=1
    return p1Wins*1.0/trials



#print(trials(100,100,{1,2},.1,strategicAI,randomAI))
print(probalisticSwitching(21, {1,2}, 0.1))
print(cache)


