import math
import random
from IsingModel import IsingModel

class Wolff(IsingModel):
    def step(self):
        random_point = self.lattice.get_random_label()
        prob_threshold = 1 - math.exp(-2 * self.j / self.temp)
        cluster = self.lattice.get_cluster(random_point, lambda label: random.random() <= prob_threshold)
        for label in cluster:
            self.lattice.set(label, -1 * self.lattice.get(label))
        self.add_flips(len(cluster))