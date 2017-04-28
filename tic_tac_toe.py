# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:37:09 2017

@author: patri
"""

pow3 = [pow(3, p) for p in range(10)]    
def basewise_bit(x, b, m):
    mm = b * m
    return (x % mm) // m
    
def three_same(x, y, z):
    if x == y and y == z:
        return x
    else:
        return 0

def tic_tac_toe_game():
    c = [0, 1, -1]
    def F(x):
        d = [basewise_bit(x, 3, pow3[p]) for p in range(9)]
        if tic_tac_toe_end_position(d) > 0:
            return set()
        else:
            t = basewise_bit(x, 3, pow3[9])
            return {x + t * pow3[p] + c[t] * pow3[9] for p in range(9) if d[p] == 0}
    return F

def tic_tac_toe_end_position(d):    
    v = three_same(d[0], d[1], d[2])
    if v > 0: return v
    
    v = three_same(d[0], d[3], d[6])
    if v > 0: return v
    
    v = three_same(d[0], d[4], d[8])
    if v > 0: return v
    
    v = three_same(d[2], d[4], d[6])
    if v > 0: return v
    
    v = three_same(d[2], d[5], d[8])
    if v > 0: return v
    v = three_same(d[8], d[7], d[6])
    
    v = three_same(d[1], d[4], d[7])
    if v > 0: return v
    
    v = three_same(d[3], d[4], d[5])
    if v > 0: return v
    
    return 0

p = 0.9
F = tic_tac_toe_game()
x = pow3[9]
bernoulli_strategy = bernoulli_g(p, x, F, dict())
naive_strategy = g(x, F, dict())


p1 = strategic_player(0.1, F, strategy)
p2 = strategic_player(0.1, F, naive_strategy)
#p2 = random_player(F)

print (bernoulli_tournement(p, x, p1, p2, 10000))




