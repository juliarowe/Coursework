import random
import copy
from Lattice import Lattice

class SquareLattice(Lattice):
    def __init__(self, size, num_dimensions):
        self.size = size
        self.num_dimensions = num_dimensions
        self.data = self.generate_array(num_dimensions)

    # Generates the internal data structure for the square lattice
    def generate_array(self, num_dimensions):
        if num_dimensions == 1:
            return [self.random_spin() for x in xrange(self.size)]
        else:
            return [self.generate_array(num_dimensions - 1) for x in xrange(self.size)]

    def get_random_label(self):
        return tuple(random.randrange(self.size) for x in xrange(self.num_dimensions))

    def export(self):
        return copy.deepcopy(self.data)

    # See Lattice superclass
    def get(self, label):
        ret = self.data
        for i in label:
            ret = ret[i]
        return ret

    # See Lattice superclass
    def set(self, label, value):
        arr = self.data
        for i in label[:-1]:
            arr = arr[i]
        arr[label[-1]] = value

    # Wraps a value to the other side of the grid
    # used to approximate an infinitely sized grid
    def wrap(self, number):
        return number % self.size

    # See Lattice superclass
    def get_neighbors(self, label):
        # The number of neighbors is twice the number of dimensions
        neighbors = [list(label) for x in xrange(2 * self.num_dimensions)]
        for i in xrange(self.num_dimensions):
            neighbors[2*i][i] = self.wrap(neighbors[2*i][i]+1)
            neighbors[2*i+1][i] = self.wrap(neighbors[2*i+1][i] - 1)
        return [tuple(x) for x in neighbors]