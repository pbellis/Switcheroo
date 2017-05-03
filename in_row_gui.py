from tkinter import *
from tkinter.font import Font
from random import random
from game import *
from in_row import *

class TK_InRowBoard(Canvas):
    def __init__(self, p, x, n, m, F, E, cpu, cpu_first, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)

        self.p = p
        self.x = x
        self.y = x
        self.n = n
        self.n_sqr = n * n
        self.m = m
        self.F = F
        self.E = E
        self. cpu = cpu
        self.cpu_first = cpu_first

        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.tile_height = self.height / n
        self.tile_width = self.width / n
        
        self.bind("<Button-1>", self.on_left_mouse_click)
        self.bind("<Button-3>", self.on_right_mouse_click)

        self.draw()
        self.pack()
        
        if (self.cpu_first):
            self.cpu_turn()

    def reset(self):
        self.x = pow3[self.n_sqr]
        self.draw()
        
        if (self.cpu_first):
            self.cpu_turn()
        
    def draw_cross(self, x, y, preview):
        color = "yellow" if preview else "red"
        self.create_line(x * self.tile_width, y * self.tile_height, (x + 1) * self.tile_width, (y + 1) * self.tile_height, fill=color, width=2)
        self.create_line(x * self.tile_width, (y + 1) * self.tile_height, (x + 1) * self.tile_width, y * self.tile_height, fill=color, width=2)
        
    def draw_circle(self, x, y, preview):
        color = "yellow" if preview else "green"
        self.create_oval(x * self.tile_width, y * self.tile_height, (x + 1) * self.tile_width, (y + 1) * self.tile_height, outline=color, fill='',width=2)
                
    def draw_tiles(self, d, preview):
        for x in range(self.n):
            for y in range(self.n):
                i = y * self.n + x
                self.create_rectangle(x * self.tile_width, y * self.tile_height, (x + 1) * self.tile_width, (y + 1) * self.tile_height, fill='', width=2)
                if d[i] == 1:
                    self.draw_cross(x, y, preview)
                elif d[i] == 2:
                    self.draw_circle(x, y, preview)
                    
    def draw(self, preview=False):
        Dx = [basewise_bit(self.x, 3, pow3[p]) for p in range(self.n_sqr)]
        self.delete(ALL)
        self.draw_tiles(Dx, False)
        
        if preview:
            Dy = [basewise_bit(self.y, 3, pow3[p]) for p in range(self.n_sqr)]
            Dy = [dy if dx != dy else 0 for (dx, dy) in zip(Dx, Dy)]
            self.draw_tiles(Dy, True)

    def write_message(self, message):
        self.create_text(self.width / 2, self.height / 2, text=message, font=Font(size=38), fill='blue')

    def on_left_mouse_click(self, event):
        if len(self.F(self.x)) == 0:
            self.reset()
            return
        
        s = [0, 1, -1]
        x = int(event.x / self.tile_width)
        y = int(event.y / self.tile_height)
        
        t = basewise_bit(self.x, 3, pow3[self.n_sqr])
        i = y * self.n + x
        self.y = self.x + t * pow3[i] + s[t] * pow3[self.n_sqr]
        
        if self.y in self.F(self.x):
            self.draw(True)

    def on_right_mouse_click(self, event):
        if len(self.F(self.x)) == 0:
            self.reset()
            return
        
        if self.y in self.F(self.x):
            self.x = self.y
            self.draw()
            
            e = self.E(self.x)
            
            if random() < self.p and e:
                self.write_message("You Lose!")
                return
            elif e:
                self.write_message("You Win!")
                return
            else:
                if (random() > self.p):
                    if self.cpu_turn():
                        return
                        
        if len(self.F(self.x)) == 0:
            self.write_message("Draw!")
            return
    
    def cpu_turn(self):
        self.cpu_pick()
        while random() < p:
            if self.E(self.x):
                self.write_message("You Win!")
                return True
            self.cpu_pick()
        if self.E(self.x):
            self.write_message("You Lose!")
            return True
        return False
    
    def cpu_pick(self):
        y = self.cpu(self.x)
        self.draw()
        if y in self.F(self.x):
            self.x = y
            self.draw()
            
if __name__ == "__main__":
    p, n, m = 0.9, 4, 3
    x, F, E, bernoulli_strategy, _ = in_row_init(p, n, m)
    cpu = strategic_player(p, F, bernoulli_strategy)

    root = Tk()
    canvas = TK_InRowBoard(p, x, n, m, F, E, cpu, True, root, bg='white', width = 512, height = 512)
    root.mainloop()
