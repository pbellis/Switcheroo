# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:28:50 2017

@author: patri
"""

from tkinter import *
from random import random
from functools import reduce
from game import *

def swap_subtraction_game(S, r):
    AS = {a + b for a in S for b in S}
    def F(x):
        n, t = x
        if t == r:
            return {(n-s, 1) for s in AS if n >= s}
        else:
            return {(n-s, t+1) for s in S if n >= s}
    return F

def subtraction_game(S):
    def F(x):
        return {x-s for s in S if x-s > -1}
    return F

class Tk_SubtractionBoard(Canvas):
    def __init__(self, p, x, F, p1, p2, strategy, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        
        self.p = p
        self.x = x
        self.F = F
        self.p1 = p1
        self.p2 = p2
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
            t = int(self.input_box.get())
        except:
            t = 0
        y = self.x - t
        if y in F(self.x):
            self.x = y
            if len(F(self.x)) > 0 and random() > self.p:
                self.x = p1(self.x)
                self.draw()
                while random() < p:
                    self.x = p1(self.x)
                    self.draw()
                    
            else:
                self.draw()
                
    def draw(self):
        self.delete(ALL)
        self.create_text(self.width * 0.5, self.height * 0.5, text=str(self.x), font=(None, min(self.width, self.height) // 4))
        

p = 0.1
F = subtraction_game({1,2})
x = 100
bernoulli_strategy = bernoulli_g(p, x, F, dict())
naive_strategy = g(x, F, dict())

p1 = strategic_player(p, F, bernoulli_strategy)
p1 = strategic_player(p, F, naive_strategy)
p2 = random_player(F)

print (tournement(p, x, p1, p1, 100000))
print (tournement(p, x, p1, p2, 100000))
print (tournement(p, x, p2, p1, 100000))
print (tournement(p, x, p2, p2, 100000))

#root = Tk()
#canvas = Tk_SubtractionBoard(p, x, F, p1, p2, bernoulli_strategy, root, bg='white', width = 512, height = 512)
#root.mainloop()

