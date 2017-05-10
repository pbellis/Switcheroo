# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:37:09 2017

@author: patri
"""

from game import *
import pickle


max_n = 8
max_n_sqr = max_n * max_n

pow3 = [pow(3, p) for p in range(max_n_sqr + 1)]    

def basewise_bit(x, b, m):
    mm = b * m
    return (x % mm) // m

#x2d = lambda x : [basewise_bit(x, 3, pow3[p]) for p in range(9)]
#d2x = lambda d : [d[p] * pow3[p] for p in range(n) if d[p] > 0]

def is_in_row_end_state(d, r, n):
    checks = (
            ((d[x + y * n] for x in range(n)) for y in range(n)),                       # row check
            ((d[x + y * n] for y in range(n)) for x in range(n)),                       # col check
            ((d[x + i + i * n] for i in range(n - x)) for x in range(n)),               # first half positive diagnol check
            ((d[i + (y + i) * n] for i in range(n - y)) for y in range(1, n)),          # second half ^
            ((d[x - i + i * n] for i in range(x + 1)) for x in range(n)),               # first half negative diagnol check
            ((d[n - i - 1 + (y + i) * n] for i in range(n - y)) for y in range(1, n))   # second half ^
            )
    for check in checks:
        for test in check:
            t, c = 0, 0
            for v in test:
                if v != t:
                    t, c = v, 1
                elif v != 0:
                    c += 1
                    if c == r:
                        return v
    return 0

def in_row_game(r, n):
    n_sqr = n * n
    s = [0, 1, -1]
     
    def F(x):
        d = [basewise_bit(x, 3, pow3[p]) for p in range(n_sqr)]
        if is_in_row_end_state(d, r, n):
            return set()
        else:
            t = basewise_bit(x, 3, pow3[n_sqr])
            return {x + t * pow3[p] + s[t] * pow3[n_sqr] for p in range(n_sqr) if d[p] == 0}
        
    def E(x):
        return is_in_row_end_state([basewise_bit(x, 3, pow3[p]) for p in range(n_sqr)], r, n) != 0
        
    return F, E

def in_row_strategy_files(x, p, n, m):
    bs_file = "SwitcherooStrategies/bernoulli_tictactoe_"+str(p)[2:]+"_"+str(n)+"_"+str(m)+"_"+str(x)+".p"
    ns_file = "SwitcherooStrategies/naive_tictactoe_"+str(n)+"_"+str(m)+"_"+str(x)+".p" 
    return bs_file, ns_file

def in_row_init(p, n, m):
    x = pow3[n*n]
    F, E = in_row_game(m, n)

    bs_file, ns_file = in_row_strategy_files(x, p, n, m) 
    
    try:
        bernoulli_strategy = pickle.load(open(bs_file, "rb"))
    except:
        print ("computing bernoulli strategy...(this could take a long time)")
        bernoulli_strategy = bernoulli_g(p, x, F, E, dict())
        pickle.dump(bernoulli_strategy, open(bs_file, "wb"))
 
    try:
        naive_strategy = pickle.load(open(ns_file, "rb"))
    except:
        print ("computing naive strategy...(this could take a long time)")
        naive_strategy = bernoulli_g(0, x, F, E, dict())
        pickle.dump(naive_strategy, open(ns_file, "wb"))
    return x, F, E, bernoulli_strategy, naive_strategy

def in_row_tournement(p, n, m, r):
    x, F, E, bernoulli_strategy, naive_strategy = in_row_init(p, n, m)
    
    p1 = strategic_player(p, F, bernoulli_strategy)
    p2 = strategic_player(0, F, naive_strategy)
    p3 = random_player(F)
    
    print ("using p =", p, "x =", x, "n =", n, "m =", m, "r =", r)
    print ("with p1 = strategic_player p2 = naive_player p3 = random_player")
    print ("results recorded, win rate, loss rate, tie rate")
    
    print ("p1 vs. p1,", str(tournement(p, x, p1, p1, r, E))[1:-1])
    
    print ("p1 vs. p2,", str(tournement(p, x, p1, p2, r, E))[1:-1])
    print ("p1 vs. p3,", str(tournement(p, x, p1, p3, r, E))[1:-1])
    
    print ("p2 vs. p1,", str(tournement(p, x, p2, p1, r, E))[1:-1])
    print ("p2 vs. p3,", str(tournement(p, x, p2, p3, r, E))[1:-1])
    
    print ("p3 vs. p1,", str(tournement(p, x, p3, p1, r, E))[1:-1])
    print ("p3 vs. p2,", str(tournement(p, x, p3, p2, r, E))[1:-1])
                                    
if __name__ == "__main__":
    for p in (i / 10 for i in range(9, 10)):
        n, m = 4, 3
        in_row_tournement(p, n, m, 10000)                
    # very inefficient
    #print ("p1 and p2", "are the same" if {p1(y) for y in bernoulli_strategy} == {p2(y) for y in bernoulli_strategy} else "are different")