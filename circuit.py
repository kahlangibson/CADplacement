import simAnneal
from random import *


class Cell:
    """ Cell object with x,y position
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circuit:
    def __init__(self, f, picture):
        [self.numCells, self.numNets, self.ny, self.nx] = [int(s) for s in f.readline().split()]

        self.nets = []
        for _ in range(self.numNets):
            line = f.readline().split()
            if len([s for s in line]) is 0:
                # empty line, read next
                line = f.readline().split()
            print line
            net = [int(line[1])]
            net.append([int(s) for s in line[2:]])
            self.nets.append(net)

        self.picture = picture
        if self.picture is not None:
            self.picture.make(self.ny, self.nx)

        self.grid = []
        for _ in range(self.ny):
            row = []
            for _ in range(self.nx):
                row.append(' ')
            self.grid.append(row)

        self.cost = 0
        self.cells = []

        self.init_place()

    def is_empty(self, x, y):
        """ Checks the status of the cell position x,y
        returns:
            False if the cell is not empty or x,y is not in the grid range
            True otherwise
        """
        if x in range(self.nx) and y in range(self.ny):
            if self.grid[y][x] == ' ':
                return True
        return False

    def put_cell(self, x, y, num):
        """ Places cell #num on the array at position x,y
        sets:
            - self.grid at x,y, and updates image with initial placement
        returns:
            False if the cell fails not_empty
            True otherwise
        """
        if self.is_empty(x,y):
            self.grid[y][x] = num
            if self.picture is not None:
                self.picture.place(x, y, num)
            return True
        return False

    def init_place(self):
        """ Places cells on the array initially
        assumes:
            - nothing has been placed before
        sets:
            - self.grid, and updates image with initial placement
            - self.cost
        asserts:
            - if failure to place cell in grid (put_cell returns False)
            - if failure to calculate cost (calc_cost returns False)
        """
        for i in range(self.numCells):
            x = randint(0,self.nx)
            y = randint(0,self.ny)
            while not self.is_empty(x,y):
                x = randint(0, self.nx)
                y = randint(0, self.ny)
            assert self.put_cell(x, y, i) is True
            self.cells.append(Cell(x,y))

        assert self.calc_cost() is True

    def calc_cost(self):
        """ Calculates the cost of current placement given net hierarchy
        assumes:
            - valid net list in self.nets
        sets:
            - self.cost
        """
        cost = 0
        if self.picture is not None:
            self.picture.clear_nets()
        for [source, sinks] in self.nets:
            cost += self.calc_half_perimeter(source, sinks)
        self.cost = cost
        if self.picture is not None:
            self.picture.update_cost(cost)
        return True

    def calc_half_perimeter(self, source, sinks):
        """ Calculates the half perimeter smallest bounding box cost of a net
        assumes:
            - valid cell positions in source, sinks
        returns:
            - self.cost
        asserts:
            - if failure to calculate cost (any cell x,y not in grid range)
        """
        deltax = 0
        deltay = 0
        assert self.cells[source].x in range(self.nx) and self.cells[source].y in range(self.ny)
        for sink in sinks:
            assert self.cells[sink].x in range(self.nx) and self.cells[sink].y in range(self.ny)
            if self.picture is not None:
                self.picture.draw_net(self.cells[source].x, self.cells[source].y, self.cells[sink].x, self.cells[sink].y)
            dx = abs(self.cells[source].x - self.cells[sink].x)
            if dx > deltax:
                deltax = dx
            dy = abs(self.cells[source].y - self.cells[sink].y)
            if dy > deltay:
                deltay = dy
        return deltax + deltay

