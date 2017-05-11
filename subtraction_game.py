# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:28:50 2017

@author: patri
"""

from tkinter import *
from random import random
from game import *
from time import sleep
from math import exp

def swap_subtraction_game(S, r):
    AS = {a + b for a in S for b in S}
    min_S = min(S)

    def F(x):
        n, t = x
        if t == r:
            return {(n-s, 1) for s in AS if n >= s}
        else:
            return {(n-s, t+1) for s in S if n >= s}
    def E(x): 
        return x < min_S
    return F, E

def subtraction_game(S):
    min_S = min(S)
    
    def F(x):
        return {x-s for s in S if x-s > -1}
    def E(x): 
        return x < min_S
    return F, E

def general_subtraction_game(S):
    min_S = min(S)
    
    def F(x):
        n,t = x
        return {(n-s,t+1) for s in S if x-s > -1}
    def E(x): 
        return x < min_S
    return F, E

class Tk_SubtractionBoard(Canvas):
    def __init__(self, p, x, F, cpu, strategy, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        
        self.p = p
        self.x = x
        self.F = F
        self.cpu = cpu
        self.strategy = strategy
        
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        
        self.input_box = Entry(master=parent)
        self.input_box.pack()
        
        self.submit_botton = Button(parent, command=self.button_click, text="Take Away!")
        self.submit_botton.pack()
        
        self.draw()
        self.pack()
        
        self.text = StringVar()
        self.message = Message(master=parent, textvariable=self.text)
        self.message.pack()
        
    def button_click(self):
        try:
            s = int(self.input_box.get())
        except:
            s = 0
            
        Y = F(x)        
        y = self.x - s
        
        if y in Y:
            self.x = y
            self.draw()
            if (random() > self.p):
                self.simulate()
    
    def simulate(self):
        sleep(0.05)
        self.x = self.cpu(self.x)
        self.draw()
        while random() < p:
            sleep(0.05)
            self.x = self.cpu(self.x)
            self.draw()
            
                
    def draw(self):
        self.delete(ALL)
        self.create_text(self.width * 0.5, self.height * 0.5, text=str(self.x), font=(None, min(self.width, self.height) // 4))
        
if __name__ == "__main__":
    p = 0.1
    S = {1,2}
    F, E = subtraction_game(S)
    x = 21
    r = 1000
    P = lambda t : 1 - exp(-t)
    
    general_strategy = general_g((21, 0), P, F, E, dict())
    bernoulli_strategy = bernoulli_g(p, x, F, E, dict())
    naive_strategy = bernoulli_g(0, x, F, E, dict())
        
    p1 = strategic_player(p, F, bernoulli_strategy)
    p2 = strategic_player(0, F, naive_strategy)
    p3 = random_player(F)
    
    print ("using p =", p, "S =", S, "x =", x, "r =", r)
    print ("with p1 = strategic_player p2 = naive_player p3 = random_player")
    print ("results recorded as p1 win rate, p2 win rate, tie rate")
    
    print ("p1 vs. p2", tournement(p, x, p1, p2, r, E))
    print ("p1 vs. p3", tournement(p, x, p1, p3, r, E))
    
    print ("p2 vs. p1", tournement(p, x, p2, p1, r, E))
    print ("p2 vs. p3", tournement(p, x, p2, p3, r, E))
    
    print ("p3 vs. p1", tournement(p, x, p3, p1, r, E))
    print ("p3 vs. p2", tournement(p, x, p3, p2, r, E))
    
    print ("p1 and p2", "are the same" if {p1(y) for y in bernoulli_strategy} == {p2(y) for y in bernoulli_strategy} else "are different")
    
    p = 0.1
    S = {1,2}
    F, E = subtraction_game(S)
    x = 21
    r = 1000
    P = lambda t : 1 - exp(-t)
    
    general_strategy = general_g((21, 0), P, F, E, dict())
    bernoulli_strategy = bernoulli_g(p, x, F, E, dict())
    naive_strategy = bernoulli_g(0, x, F, E, dict())
        
    p1 = general_strategic_player(P, F, general_strategy)
    p2 = strategic_player(0, F, naive_strategy)
    p3 = random_player(F)
    
    print ("using p =", p, "S =", S, "x =", x, "r =", r)
    print ("with p1 = general_strategic_player p2 = stratigic_player p3 = random_player")
    print ("results recorded as p1 win rate, p2 win rate, tie rate")
    
    print ("p1 vs. p2", gen_tournement(P, x, p1, p2, r, E))
    print ("p1 vs. p3", gen_tournement(P, x, p1, p3, r, E))
    
    print ("p2 vs. p1", gen_tournement(P, x, p2, p1, r, E))
    print ("p2 vs. p3", gen_tournement(P, x, p2, p3, r, E))
    
    print ("p3 vs. p1", gen_tournement(P, x, p3, p1, r, E))
    print ("p3 vs. p2", gen_tournement(P, x, p3, p2, r, E))