# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:24:23 2017

@author: patri
"""

from random import sample, random
from math import log

def mex(Y):
    if len(Y) == 0:
        return 0
    else:
        m = max(Y)
        for x in range(m+2):
            if not x in Y:
                return x

def g(x, F, memo):
    if x in memo:
        return memo
    else:
        Y = F(x)
        r = {g(y, F, memo)[y] for y in Y}       
        memo[x] = mex(r)
        return memo
            
def bernoulli_g(p, x, F, E, memo):
    if x in memo:
        return memo
    else:
        Y = F(x)

        if len(Y) == 0:
            memo[x] = 0 if E(x) else 0.5
            return memo
        else:
            r = (bernoulli_g(p, y, F, E, memo)[y] for y in Y)
            memo[x] = max(((1 - a) * (1- p) + a * p for a in r))
            return memo

# x is state
# P is P(t) is probability given t times since swap
# F is follower function
# E is End State function (if win or loss or tie)
def general_g(xt, P, F, E, memo):
    if xt in memo:
        return memo
    else:    
        x, t = xt
        Y = F(x)
                
        if len(Y) == 0:
            memo[xt] = 0 if E(x) else 0.5
            return memo
        else:
            p = P(t)
            rkes = [general_g((y, t+1), P, F, E, memo)[(y,t+1)] for y in Y]
            rses = [general_g((y, 0), P, F, E, memo)[(y,0)] for y in Y]
            memo[xt] = max(((1 - rk) * (1 - p) + rs * p for rk, rs in zip(rkes, rses)))
            return memo

def strategic_entropy(x, F, strategy):
    decisions = [strategy[y] for y in F(x)]
    total = sum(decisions)
    entropy = 0
    for decision in decisions:
        p = decision / total
        entropy -= p * log(p, len(decisions))
    return entropy

def naive_player(F, strategy):
    def naive_next_move(x):
        Y = F(x)
        if len(Y) == 0:
            return None
        else:
            return min(Y, key=lambda y: strategy[y])
    return naive_next_move
            
def strategic_player(p, F, strategy):
    def strategic_next_move(x):
        Y = F(x)
        if len(Y) == 0:
            return None
        else:
            return max(Y, key=lambda y: (1 - strategy[y]) * (1 - p) + strategy[y] * p)
    return strategic_next_move

def general_strategic_player(P, F, strategy):
    def strategic_next_move(x):
        n,t = x
        Y = F(n)
        if len(Y) == 0:
            return None
        else:
            return max(Y, key=lambda y: (1 - strategy[y,t+1]) * (1 - P(t)) + strategy[y,0] * P(t))
    return strategic_next_move

def random_player(F):
    def random_next_move(x):
        Y = F(x)
        return None if len(Y) == 0 else sample(Y, 1)[0]
    return random_next_move
        
def simulate(p, x, p1, p2, E):
    T = [1, 0]
    P = [p1, p2]
    
    t = 0
    y = P[t](x)
    while y != None:
        x = y
        if (random() > p) :
            t = T[t]
        y = P[t](x)

    if E(x):
        return T[t]
    else:
        return 2 

def tournement(p, x, p1, p2, r, E):
    W = [0, 0, 0]
    for i in range(r):
        W[simulate(p, x, p1, p2, E)] += 1
    return W[0] / r, W[1] / r, W[2] / r

def generalSimulate(Pr,x,p1,p2,E):
    T = [1, 0]
    P = [p1, p2]
    t = 0
    turn = 0
    try:
        y = P[t](x)
    except(TypeError):
        y = P[t]((x,turn))

    while y != None:
        x = y
        if (random() > Pr(turn)) :
            t = T[t]
            turn+=1
        else:
            turn = 0
        try:
            y = P[t](x)
        except(TypeError):
            y = P[t]((x,turn))

    if E(x):
        return T[t]
    else:
        return 2 
    
def gen_tournement(Pr, x, p1, p2, r, E):
    W = [0, 0, 0]
    for i in range(r):
        W[generalSimulate(Pr, x, p1, p2, E)] += 1
    return W[0] / r, W[1] / r, W[2] / r
