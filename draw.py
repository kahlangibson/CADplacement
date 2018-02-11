from Tkinter import *
import Tkinter as tk

class draw:
    def __init__(self, parent):
        self.myParent = parent

        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)

        self.cellwidth = 0
        self.cellheight = 0
        self.rect = {}
        self.text = {}
        self.lines = []
        self.costy = 0
        self.cost = 0

    def delete(self):
        self.myCanvas.delete('all')
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)

    def clear_nets(self):
        for each in self.lines:
            self.myCanvas.delete(each)

    def make(self, rows, columns):
        bigger = max(columns, rows)
        self.cellwidth = 500/bigger
        self.cellheight = 500/bigger
        self.buffer = 500/(10*bigger)

        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,
                                width=(self.cellheight+self.buffer)*columns + self.buffer,
                                height=(self.cellwidth+self.buffer)*rows + self.buffer + 50)
        self.myCanvas.pack(side=tk.RIGHT)

        for column in range(rows):
            for row in range(columns):
                x1 = column * (self.cellwidth + self.buffer) + self.buffer
                y1 = row * (self.cellheight + self.buffer) + self.buffer
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row, column] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="white")

        self.costy = rows * (self.cellheight + self.buffer) + self.buffer
        self.text[10,self.costy] = self.myCanvas.create_text(20, self.costy, text="Cost: ")
        self.cost = self.myCanvas.create_text(50, self.costy, text=0)

    def place(self, x, y, num):
        x1 = x * (self.cellwidth + self.buffer) + self.buffer
        y1 = y * (self.cellheight + self.buffer) + self.buffer
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight
        self.text[x, y] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, text=num)

    def draw_net(self, x1, y1, x2, y2):
        startx = x1 * (self.cellwidth + self.buffer) + self.buffer + self.cellwidth/2
        starty = y1 * (self.cellheight + self.buffer) + self.buffer + self.cellheight/2
        endx = x2 * (self.cellwidth + self.buffer) + self.buffer + self.cellwidth/2
        endy = y2 * (self.cellheight + self.buffer) + self.buffer + self.cellheight/2
        self.lines.append(self.myCanvas.create_line(startx,starty,endx,endy,arrow=LAST))

    def update_cost(self, cost):
        self.myCanvas.delete(self.cost)
        self.cost = self.myCanvas.create_text(50, self.costy, text=cost)
