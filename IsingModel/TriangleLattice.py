from Lattice import Lattice
import random
import copy

class TriangleLattice(Lattice):
    def __init__(self, size, num_dimensions):
        self.size = size
        self.data = [[self.random_spin() for y in xrange(self.size)] for x in xrange(self.size)]

    def get(self, (i, j)):
        return self.data[i][j]

    def set(self, (i, j), value):
        self.data[i][j] = value

    def get_random_label(self):
        return (random.randrange(self.size), random.randrange(self.size))

    def export(self):
        return copy.deepcopy(self.data)

    def wrap(self, number):
        return number % self.size

    def get_neighbors(self, (i,j)):
        # If we're in an even row or odd row, change what are neighbors are
        neighbors = [(i-1, j),(i+1, j),(i, j-1),(i, j+1),(i+1, j-1),(i+1, j+1)] if j % 2 == 0 else [(i-1, j),(i+1, j),(i, j-1),(i, j+1),(i-1, j-1),(i-1, j+1)]
        return [(self.wrap(x), self.wrap(y)) for (x, y) in neighbors]