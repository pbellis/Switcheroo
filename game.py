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
    
def bernoulli_g(p, x, F, memo):
    if x in memo:
        return memo
    else:
        Y = F(x)

        if len(Y) == 0:
            memo[x] = 0
            return memo
        else:
            r = [bernoulli_g(p, y, F, memo)[y] for y in Y]
            c = (max if p > 0.5 else min)(r)
            l = (1 - c) * (1 - p)
            w = c * p
            memo[x] = l + w
            return memo

def strategic_entropy(x, F, strategy):
    decisions = [strategy[y] for y in F(x)]
    total = sum(decisions)
    entropy = 0
    for decision in decisions:
        p = decision / total
        entropy -= p * log(p, len(decisions))
    return entropy
        
def strategic_player(p, F, strategy):
    choose = max if p > 0.5 else min
    def strategic_next_move(x):
        Y = F(x)
        return None if len(Y) == 0 else choose(Y, key=lambda y: strategy[y])  
    return strategic_next_move

def random_player(F):
    def random_next_move(x):
        Y = F(x)
        return None if len(Y) == 0 else sample(Y, 1)[0]
    return random_next_move
        
def simulate(p, x, p1, p2):
    T = [1, 0]
    P = [p1, p2]
    t = 0
    while True:
        x = P[t](x)
        if (random() > p) :
            t = T[t]
        if x == None:
            break
    return t 

def tournement(p, x, p1, p2, rounds):
    count = 0
    for i in range(rounds):
        count += simulate(p, x, p1, p2)
    return count / rounds