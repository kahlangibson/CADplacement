from math import *
from random import *
from circuit import *

class simAnneal(Circuit):
    def __init__(self, startT, n, deltaT, Treq, runWith0, f, picture):
        Circuit.__init__(f,picture)
        self.startT = startT
        self.n = n
        self.deltaT = deltaT
        self.Treq = Treq
        self.runWith0 = runWith0

    def runSimAnneal(self):
        temp = self.startT
        while True:
            for _ in range(self.n):
                # randomly choose 2 cells
                [cell1, cell2] = sample(self.cells, 2)
                # calculate new cost of switch
                deltaC = self.compare_switch_cost(cell1,cell2)
                # generate random number
                r = random()
                if r < exp(-deltaC/temp):
                    self.keep_switch(cell1,cell2)
            temp = temp - self.deltaT
            if temp <= self.Treq:
                if self.runWith0:
                    temp = 0
                else:
                    break
            elif temp == 0:
                break
