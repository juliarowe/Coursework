from IsingModel import IsingModel
import random
import math

class Metropolis(IsingModel):
    # Given a change in energy, returns a boolean which tells whether or not
    # the spin should flip in the Metropolis model
    def should_change_spins(self, delta_e):
        if delta_e <= 0:
            # Always make the proposed change if the energy of the system
            # decreases if the change was to be made
            return True
        else:
            change_probability = math.exp(-delta_e / self.temp)
            return random.random() <= change_probability

    def step(self):
        label = self.lattice.get_random_label()
        spin = self.lattice.get(label)
        neighbor_spins = [self.lattice.get(neighbor) for neighbor in self.lattice.get_neighbors(label)]
        # j is the exchange parameter
        partial_hamiltonian = self.j * sum(neighbor_spins)
        h_before = spin * partial_hamiltonian
        h_after = -1 * spin * partial_hamiltonian
        delta_e = h_after - h_before
        if self.should_change_spins(delta_e):
            self.lattice.set(label, -1 * spin)
        self.add_flips(1)