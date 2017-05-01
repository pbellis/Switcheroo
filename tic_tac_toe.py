# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:37:09 2017

@author: patri
"""
from game import *

max_n = 8
max_n_sqr = max_n * max_n

pow3 = [pow(3, p) for p in range(max_n_sqr + 1)]    

def basewise_bit(x, b, m):
    mm = b * m
    return (x % mm) // m

#x2d = lambda x : [basewise_bit(x, 3, pow3[p]) for p in range(9)]
#d2x = lambda d : [d[p] * pow3[p] for p in range(n) if d[p] > 0]
    
def in_row_game(r, n):
    n_sqr = n * n
    s = [0, 1, -1]
               
    def E(d):
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
     
    def F(x):
        d = [basewise_bit(x, 3, pow3[p]) for p in range(n_sqr)]
        if E(d):
            return set()
        else:
            t = basewise_bit(x, 3, pow3[n_sqr])
            return {x + t * pow3[p] + s[t] * pow3[n_sqr] for p in range(n_sqr) if d[p] == 0}
    return F, lambda x : E([basewise_bit(x, 3, pow3[p]) for p in range(n_sqr)])

p = 0.9
F, E = in_row_game(3, 3)
x = pow3[9]
bernoulli_strategy = bernoulli_g(p, x, F, dict())
naive_strategy = g(x, F, dict())

p1 = strategic_player(p, F, bernoulli_strategy)
p2 = strategic_player(p, F, naive_strategy)
#p2 = random_player(F)

print (tournement(p, x, p1, p2, 10000))



