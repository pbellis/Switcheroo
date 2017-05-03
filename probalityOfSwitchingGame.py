cache = {0:(0.0,0)}
from random import sample, random
from game import *
from subtraction_game import *

#max_debug = dict()

def probalisticSwitching(chips,subtractionSet,p):
    if chips in cache:
        return cache[chips]
    else:
        possiblePositions = [(s,chips-s) for s in subtractionSet if (chips-s)>=0]#calculate the possible positions
        possibleProbabilitiesIfSucess = [(position[0],probalisticSwitching(position[1],subtractionSet,p)[1]) for position in possiblePositions]
        probabilityWinWithS = [(probSucess[0],(((1-probSucess[1])*(1-p))+probSucess[1]*p)) for probSucess in possibleProbabilitiesIfSucess]
        bestTakeAway = max(probabilityWinWithS,key=lambda x:x[1])
        #max_debug[chips] = set(probabilityWinWithS)
        cache[chips]=bestTakeAway
        return bestTakeAway

def strategicAI(chips,subtractionSet,p):
    return probalisticSwitching(chips,subtractionSet,p)[0]

def randomAI(chips,subtractionSet,p):
    return sample(subtractionSet,1)[0]


def game(numberOfChips,subtractionSet,p,P1,P2):#player 1 starts, pass a method that returns an int in the subtraction set from the input of chips,subtractionset,p
    p1Turn = True
    while(numberOfChips>0):
        if(p1Turn):
            p1Move = P1(numberOfChips,subtractionSet,p)
            numberOfChips=max(numberOfChips-p1Move,0)#don't go below zero but subtract the players move
        else:
            p2Move = P2(numberOfChips,subtractionSet,p)
            numberOfChips=max(numberOfChips-p2Move,0)#don't go below zero but subtract the players move
        
        if(random()>p):
            p1Turn = not p1Turn
    return p1Turn # true if p1 loses, false if p1 wins

            
    

def trials(trials,numberOfChips,subtractionSet,p,P1,P2):
    p1Wins = 0
    for i in range(trials):
        if(not game(numberOfChips,subtractionSet,p,P1,P2)):#p1 wins 
            p1Wins+=1
    return p1Wins / trials


naive_strategy = g(21, subtraction_game({1,2,3}), dict())
naive_ai = naive_player(subtraction_game({1,2,3}), naive_strategy)
def naiveAI(chips, subtractionSet, p):
    return chips - naive_ai(chips)


print(trials(1000, 20,{1,2,3},.1,strategicAI, naiveAI))
#print(cache)


