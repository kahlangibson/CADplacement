from math import *
from random import *
from circuit import *

class simAnneal(Circuit):
    def __init__(self, startT, n, deltaT, Treq, runWith0, f, picture):
        Circuit.__init__(self, f, picture)
        self.startT = startT
        self.n = n
        self.deltaT = deltaT
        self.Treq = Treq
        self.runWith0 = runWith0

    def runSimAnneal(self):
        temp = self.startT
        while True:
            for _ in range(self.n):
                # randomly choose 2 cells - until at least one is not empty
                while True:
                    [x1, x2, y1, y2] = sample(range(self.nx), 2) + sample(range(self.ny), 2)
                    if not self.is_empty(x1, y1) or not self.is_empty(x2, y2):
                        break
                # calculate new cost of switch
                deltaC = self.compare_switch_cost(x1, y1, x2, y2)
                # generate random number
                r = random()
                # if random number is less than probability function, keep switch
                if r < exp(-deltaC/temp):
                    self.switch(x1, y1, x2, y2)
            temp = temp - self.deltaT
            if temp <= self.Treq:
                if self.runWith0:
                    for _ in range(self.n):
                        while True:
                            [x1, x2, y1, y2] = sample(range(self.nx), 2) + sample(range(self.ny), 2)
                            if not self.is_empty(x1, y1) or not self.is_empty(x2, y2):
                                break
                        # calculate new cost of switch
                        deltaC = self.compare_switch_cost(x1, y1, x2, y2)
                        if deltaC < 0:
                            self.switch(x1, y1, x2, y2)
                break
            elif temp == 0:
                break
